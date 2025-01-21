variable "cloud_id" {
  type        = string
  description = "ID облака"
}

variable "folder_id" {
  type        = string
  description = "ID каталога"
}

variable "tg_bot_key" {
  type        = string
  description = "Токен для доступа к Telegram Bot API"
}

variable "sa_key_file_path" {
  type        = string
  description = "Путь для Провайдер «Yandex.Cloud Provider» чтобы искать авторизованный ключ "
  default     = "/Users/n.maryin/Developer/Cloud_1HW/.venv/key.json"
}

variable "bucket_name" {
  type        = string
  description = "Название бакета, в котором находится объект с инструкцией к YandexGPT"
}

variable "bucket_object_key" {
  type        = string
  description = "Ключ объекта, в котором написана инструкция к YandexGPT"
  default     = "instruction.txt"
}