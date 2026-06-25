import 'chat_response.dart';

enum Sender { user, assistant }

/// A single entry in the on-screen chat history. Assistant entries carry the
/// full structured [ChatResponse] so the dynamic renderer can build the
/// right widget for it.
class ChatMessage {
  final Sender sender;
  final String text;
  final ChatResponse? response;

  ChatMessage.user(this.text)
      : sender = Sender.user,
        response = null;

  ChatMessage.assistant(this.response)
      : sender = Sender.assistant,
        text = response?.message ?? '';
}
