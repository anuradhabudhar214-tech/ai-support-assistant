import 'dart:math';

import 'package:flutter/material.dart';

import 'models/chat_message.dart';
import 'services/api_service.dart';
import 'widgets/chat_bubble.dart';
import 'widgets/chat_input.dart';

void main() {
  runApp(const SupportAssistantApp());
}

class SupportAssistantApp extends StatelessWidget {
  const SupportAssistantApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Support Assistant',
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.indigo,
      ),
      home: const ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final ApiService _api = ApiService();
  final List<ChatMessage> _messages = [];
  final ScrollController _scrollController = ScrollController();
  late final String _sessionId;
  bool _isSending = false;

  @override
  void initState() {
    super.initState();
    _sessionId = _generateSessionId();
  }

  String _generateSessionId() {
    final rand = Random();
    return 'session-${DateTime.now().millisecondsSinceEpoch}-${rand.nextInt(99999)}';
  }

  Future<void> _handleSend(String text) async {
    setState(() {
      _messages.add(ChatMessage.user(text));
      _isSending = true;
    });
    _scrollToBottom();

    final response = await _api.sendMessage(message: text, sessionId: _sessionId);

    if (!mounted) return;
    setState(() {
      _messages.add(ChatMessage.assistant(response));
      _isSending = false;
    });
    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 250),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _resetConversation() async {
    await _api.resetSession(_sessionId);
    setState(() => _messages.clear());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Support Assistant'),
        actions: [
          IconButton(
            tooltip: 'Reset conversation',
            onPressed: _resetConversation,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: _messages.isEmpty
                ? const _EmptyState()
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) => ChatBubble(message: _messages[index]),
                  ),
          ),
          const Divider(height: 1),
          ChatInput(onSend: _handleSend, isSending: _isSending),
        ],
      ),
    );
  }
}

class _EmptyState extends StatelessWidget {
  const _EmptyState();

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text(
        'Start typing a message below.',
        style: TextStyle(color: Colors.grey),
      ),
    );
  }
}