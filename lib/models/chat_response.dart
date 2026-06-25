class ChatResponse {
  final String intent;
  final String? toolCalled;
  final String uiType;
  final String message;
  final Map<String, dynamic> data;
  final String sessionId;
  final int turn;

  ChatResponse({
    required this.intent,
    required this.toolCalled,
    required this.uiType,
    required this.message,
    required this.data,
    required this.sessionId,
    required this.turn,
  });

  factory ChatResponse.fromJson(Map<String, dynamic> json) {
    return ChatResponse(
      intent: json['intent'] as String? ?? 'unknown',
      toolCalled: json['tool_called'] as String?,
      uiType: json['ui_type'] as String? ?? 'fallback',
      message: json['message'] as String? ?? '',
      data: (json['data'] as Map<String, dynamic>?) ?? const {},
      sessionId: json['session_id'] as String? ?? 'default',
      turn: json['turn'] as int? ?? 0,
    );
  }

  /// Used to construct a graceful client-side fallback response when the
  /// backend is unreachable, so the UI never crashes on network errors.
  factory ChatResponse.error(String sessionId, String reason) {
    return ChatResponse(
      intent: 'unknown',
      toolCalled: null,
      uiType: 'fallback',
      message: 'Something went wrong talking to the assistant: $reason',
      data: const {},
      sessionId: sessionId,
      turn: 0,
    );
  }
}
