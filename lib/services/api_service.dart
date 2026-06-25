import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/chat_response.dart';


class ApiService {
  static const String _defaultBaseUrl = 'http://localhost:8000';

  final String baseUrl;
  final http.Client _client;

  ApiService({String? baseUrl, http.Client? client})
      : baseUrl = baseUrl ??
            const String.fromEnvironment('API_BASE_URL', defaultValue: _defaultBaseUrl),
        _client = client ?? http.Client();

  Future<ChatResponse> sendMessage({
    required String message,
    required String sessionId,
  }) async {
    final uri = Uri.parse('$baseUrl/chat');
    try {
      final response = await _client
          .post(
            uri,
            headers: const {'Content-Type': 'application/json'},
            body: jsonEncode({'message': message, 'session_id': sessionId}),
          )
          .timeout(const Duration(seconds: 20));

      if (response.statusCode != 200) {
        return ChatResponse.error(
          sessionId,
          'Server returned status ${response.statusCode}',
        );
      }

      final decoded = jsonDecode(response.body) as Map<String, dynamic>;
      return ChatResponse.fromJson(decoded);
    } catch (e) {
      // Graceful fallback UI instead of crashing on network/parse errors.
      return ChatResponse.error(sessionId, e.toString());
    }
  }

  Future<void> resetSession(String sessionId) async {
    final uri = Uri.parse('$baseUrl/chat/reset?session_id=$sessionId');
    try {
      await _client.post(uri).timeout(const Duration(seconds: 10));
    } catch (_) {
      // Resetting memory is best-effort; ignore failures.
    }
  }
}