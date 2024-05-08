from enum import Enum
from confz import BaseConfig
from pydantic import NonNegativeInt, AnyUrl, UrlConstraints, NonNegativeFloat
from typing import List, Dict
from typing_extensions import Annotated


S3Url = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["s3"])]

BASE_INPUT_S3_URL = "s3://nu-olivia-data/avatar/input"


class ArchitectureConfig(BaseConfig):
    embedding_dim: NonNegativeInt
    attributes_max_length: NonNegativeInt
    event_window_size: NonNegativeInt
    sequence_model_num_layers: NonNegativeInt
    language_model_num_layers: NonNegativeInt


class TokenizerConfig(BaseConfig):
    event_attributes_tokenizer_path: S3Url
    event_types_vocab_path: S3Url


class StreamingPathsConfig(BaseConfig):
    train_streaming_dataset_path: S3Url
    valid_streaming_dataset_path: S3Url


class LearningTaskConfig(BaseConfig):
    train_binary_tasks: List[str]
    train_regression_tasks: List[str]
    train_losses_alphas: Dict[str, float]


class StreamingConfig(BaseConfig):
    shuffle_shards: bool = False
    read_buffer_size: NonNegativeInt


class DataLoaderConfig(BaseConfig):
    num_workers: NonNegativeInt
    prefetch_factor: NonNegativeInt
    streaming: StreamingConfig


class BufferShuffleConfig(BaseConfig):
    enable_buffer_shuffle: bool
    shuffle_buffer_size: NonNegativeInt


class Precision(str, Enum):
    fp16 = "16-mixed"
    bfp16 = "b16-mixed"


class MatMulPrecision(str, Enum):
    highest = "highest"
    high = "high"
    medium = "medium"


class TrainingConfig(BaseConfig):
    seed: NonNegativeInt
    mini_batch_size: NonNegativeInt
    grad_accumulation_steps: NonNegativeInt
    max_steps: NonNegativeInt
    limit_val_batches: NonNegativeInt
    val_check_interval: NonNegativeInt
    gradient_clip_val: NonNegativeFloat
    precision: Precision
    matmul_precision: MatMulPrecision
    tokenizer: TokenizerConfig
    streaming_paths: StreamingPathsConfig
    architecture: ArchitectureConfig
    learning_task: LearningTaskConfig
    buffer_shuffle: BufferShuffleConfig
    train_dataloader: DataLoaderConfig
    valid_dataloader: DataLoaderConfig


class ScoringConfig(BaseConfig):
    batch_size: NonNegativeInt
    num_workers: NonNegativeInt
    matmul_precision: MatMulPrecision
    score_on_cpu: bool
    streaming_config: StreamingConfig
    tokenizer: TokenizerConfig
    ckpt_path: S3Url


class MLFlowSecretsConfig(BaseConfig):
    secret_path: S3Url
    experiment_name: str


class AvatarConfig(BaseConfig):
    training: TrainingConfig
    scoring: ScoringConfig
    mlflow_secrets: MLFlowSecretsConfig
