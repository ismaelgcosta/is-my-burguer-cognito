resource "aws_sqs_queue" "is-my-burguer-pagamento-queue" {
  name                    = "is-my-burguer-pagamento-queue.fifo"
  sqs_managed_sse_enabled = true

  content_based_deduplication = true
  fifo_queue                  = true

  message_retention_seconds  = 1209600

  deduplication_scope = "queue"
}

resource "aws_sqs_queue" "is-my-burguer-pedido-queue" {
  name                    = "is-my-burguer-pedido-queue.fifo"
  sqs_managed_sse_enabled = true

  content_based_deduplication = true
  fifo_queue                  = true

  message_retention_seconds  = 1209600

  deduplication_scope = "queue"
}