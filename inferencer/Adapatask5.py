from inferencer.Inferencer import Inferencer
import os
import torch
import numpy as np
import torch.nn as nn
import torchvision.models
import librosa
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import requests


class Task5Model(nn.Module):

    def __init__(self, num_classes):
        super().__init__()
        self.bw2col = nn.Sequential(
            nn.BatchNorm2d(1),
            nn.Conv2d(1, 10, 1, padding=0), nn.ReLU(),
            nn.Conv2d(10, 3, 1, padding=0), nn.ReLU())

        self.mv2 = torchvision.models.mobilenet_v2(pretrained=True)

        self.final = nn.Sequential(
            nn.Linear(1280, 512), nn.ReLU(), nn.BatchNorm1d(512),
            nn.Linear(512, num_classes))

    def forward(self, x):
        x = self.bw2col(x)
        x = self.mv2.features(x)
        x = x.max(dim=-1)[0].max(dim=-1)[0]
        x = self.final(x)
        return x


class AudioDataset(Dataset):
    def __init__(self, X):
        self.X = X

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        sample = self.X[idx, ...]
        i = np.random.randint(sample.shape[1])
        sample = torch.cat([
            sample[:, i:, :],
            sample[:, :i, :]],
            dim=1)
        return sample


class DcaseAdapatask5(Inferencer):

    def __init__(self):
        self.device = None
        self.model = None
        self.data_path = None

        try:
            self.data_path = 'data/'
            model_name = 'model_system1'
            if (not os.path.isfile(self.data_path + model_name)):
                print('Downloading model')
                r = requests.get('https://github.com/sainathadapa/'
                                 'dcase2019-task5-urban-sound-tagging/releases/download/1.0/model_system1')
                open(self.data_path + model_name, 'wb').write(r.content)

            self.device = torch.device(os.environ['DEVICE_NAME'])
            self.model = Task5Model(31).to(self.device)
            self.model.load_state_dict(
                torch.load(self.data_path + model_name, map_location=os.environ['DEVICE_NAME']))
            self.channel_means = np.load(self.data_path + 'channel_means.npy')
            self.channel_stds = np.load(self.data_path + 'channel_stds.npy')

        except Exception as e:
            print('Error Iniciando el inferenciador ' + str(e))
            raise

    def runInferencer(self, filename, audio, samplerate):

        try:

            logmel = self.compute_melspec(audio, samplerate)
            X = np.expand_dims(logmel.T[:635, :], axis=0)
            X = X[:, None, :, :]
            X = (X - self.channel_means) / self.channel_stds
            dataset = AudioDataset(torch.Tensor(X))
            loader = DataLoader(dataset, 64, shuffle=False)

            all_preds = []
            for _ in range(10):
                preds = []
                for inputs in loader:
                    inputs = inputs.to(self.device)
                    with torch.set_grad_enabled(False):
                        self.model = self.model.eval()
                        outputs = self.model(inputs)
                        preds.append(outputs.detach().cpu().numpy())
                preds = np.concatenate(preds, axis=0)
                preds = (1 / (1 + np.exp(-preds)))
                all_preds.append(preds)
            tmp = all_preds[0]
            for x in all_preds[1:]:
                tmp += x
            tmp = tmp / 10
            preds = tmp

            output_df = pd.DataFrame(
                preds, columns=[
                    'engine', 'machinery-impact', 'non-machinery-impact',
                    'powered-saw', 'alert-signal', 'music', 'human-voice', 'dog',
                    'small-sounding-engine', 'medium-sounding-engine',
                    'large-sounding-engine', 'rock-drill', 'jackhammer',
                    'hoe-ram', 'pile-driver', 'non-machinery-impact',
                    'chainsaw', 'small-medium-rotating-saw',
                    'large-rotating-saw', 'car-horn', 'car-alarm', 'siren',
                    'reverse-beeper', 'stationary-music', 'mobile-music',
                    'ice-cream-truck', 'person-or-small-group-talking',
                    'person-or-small-group-shouting', 'large-crowd',
                    'amplified-speech', 'dog-barking-whining'])
            output_df['audio_filename'] = pd.Series(filename, index=output_df.index)

            for x in [
                'engine-of-uncertain-size', 'other-unknown-impact-machinery',
                'other-unknown-powered-saw', 'other-unknown-alert-signal',
                'music-from-uncertain-source', 'other-unknown-human-voice']:
                output_df[x] = 0

            cols_in_order = [
                "audio_filename", "small-sounding-engine",
                "medium-sounding-engine", "large-sounding-engine",
                "engine-of-uncertain-size", "rock-drill",
                "jackhammer", "hoe-ram", "pile-driver",
                "other-unknown-impact-machinery", "non-machinery-impact",
                "chainsaw", "small-medium-rotating-saw",
                "large-rotating-saw", "other-unknown-powered-saw",
                "car-horn", "car-alarm", "siren", "reverse-beeper",
                "other-unknown-alert-signal", "stationary-music",
                "mobile-music", "ice-cream-truck",
                "music-from-uncertain-source", "person-or-small-group-talking",
                "person-or-small-group-shouting", "large-crowd",
                "amplified-speech", "other-unknown-human-voice",
                "dog-barking-whining", "engine", "machinery-impact",
                "non-machinery-impact", "powered-saw", "alert-signal",
                "music", "human-voice", "dog"]
            output_df = output_df.loc[:, cols_in_order]

            return output_df.iloc[0]

        except Exception as e:
            print('An error was found ' + str(e))
            raise

    def compute_melspec(self, audio, samplerate):
        wav = librosa.resample(audio, orig_sr=samplerate, target_sr=44100)
        melspec = librosa.feature.melspectrogram(
            wav,
            sr=44100,
            n_fft=128 * 20,
            hop_length=347 * 2,
            n_mels=128,
            fmin=20,
            fmax=44100 // 2)
        logmel = librosa.core.power_to_db(melspec)
        return logmel
