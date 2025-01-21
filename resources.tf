resource "yandex_function" "vvot27_exam_solver_tg_bot" {
  name               = "vvot27-exam-solver-tg-bot"
  entrypoint         = "handle.handler"
  memory             = "128"
  runtime            = "python312"
  service_account_id = yandex_iam_service_account.vvot27_exam_solver_tg_bot.id
  user_hash          = data.archive_file.content.output_sha512
  execution_timeout  = "30"
  environment = {
    TELEGRAM_BOT_TOKEN = var.tg_bot_key
    FOLDER_ID          = var.folder_id
    MOUNT_POINT        = var.bucket_name
    BUCKET_OBJECT_KEY  = var.bucket_object_key
  }
  content {
    zip_filename = data.archive_file.content.output_path
  }
  mounts {
    name = var.bucket_name
    mode = "ro"
    object_storage {
      bucket = yandex_storage_bucket.exam_solver_tg_bot_bucket.bucket
    }
  }
}

resource "yandex_function_iam_binding" "exam_solver_tg_bot_iam" {
  function_id = yandex_function.vvot27_exam_solver_tg_bot.id
  role        = "functions.functionInvoker"
  members = [
    "system:allUsers",
  ]
}

data "http" "set_webhook_tg" {
  url = "https://api.telegram.org/bot${var.tg_bot_key}/setWebhook?url=https://functions.yandexcloud.net/${yandex_function.vvot27_exam_solver_tg_bot.id}"
}

resource "telegram_bot_webhook" "exam_solver_tg_bot_webhook" {
  url = "https://functions.yandexcloud.net/${yandex_function.vvot27_exam_solver_tg_bot.id}"
}

resource "yandex_storage_bucket" "exam_solver_tg_bot_bucket" {
  bucket = var.bucket_name
}

resource "yandex_storage_object" "yandexgpt_instruction" {
  bucket = yandex_storage_bucket.exam_solver_tg_bot_bucket.id
  key    = var.bucket_object_key
  source = "instruction.txt"
}

resource "yandex_iam_service_account" "vvot27_exam_solver_tg_bot" {
  name = var.bucket_name
}

resource "yandex_resourcemanager_folder_iam_member" "sa_exam_solver_tg_bot_ai_vision_iam" {
  folder_id = var.folder_id
  role      = "ai.vision.user"
  member    = "serviceAccount:${yandex_iam_service_account.vvot27_exam_solver_tg_bot.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "sa_exam_solver_tg_bot_ai_language_models_iam" {
  folder_id = var.folder_id
  role      = "ai.languageModels.user"
  member    = "serviceAccount:${yandex_iam_service_account.vvot27_exam_solver_tg_bot.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "sa_exam_solver_tg_bot_storage_viewer_iam" {
  folder_id = var.folder_id
  role      = "storage.viewer"
  member    = "serviceAccount:${yandex_iam_service_account.vvot27_exam_solver_tg_bot.id}"
}