import 'package:flutter/material.dart';

/// Generic key/value card renderer used for the simpler ui_types
/// (tracking_page, refund_page, complaint_page, escalation_page).
///
/// Each of these intents returns a single nested object in `data`
/// (e.g. data['tracking'], data['refund']) — this widget renders it as a
/// labeled card so every backend field is visible without bespoke widgets
/// for each one. Swap in a dedicated widget per intent later if richer UI
/// is needed (the dynamic renderer's switch statement makes that a one-line
/// change — see DynamicRenderer).
class SimpleCardWidget extends StatelessWidget {
  final String title;
  final IconData icon;
  final Map<String, dynamic> fields;

  const SimpleCardWidget({
    super.key,
    required this.title,
    required this.icon,
    required this.fields,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(14.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: Theme.of(context).colorScheme.primary),
                const SizedBox(width: 8),
                Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              ],
            ),
            const Divider(height: 16),
            ...fields.entries
                .where((e) => e.key != 'history')
                .map(
                  (e) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 2),
                    child: Row(
                      children: [
                        Expanded(
                          flex: 2,
                          child: Text(
                            _label(e.key),
                            style: const TextStyle(color: Colors.grey),
                          ),
                        ),
                        Expanded(
                          flex: 3,
                          child: Text(e.value.toString(), textAlign: TextAlign.right),
                        ),
                      ],
                    ),
                  ),
                ),
            if (fields['history'] is List)
              ...List<Widget>.from(
                (fields['history'] as List).map(
                  (stage) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 2),
                    child: Row(
                      children: [
                        Icon(
                          (stage['done'] == true) ? Icons.check_circle : Icons.radio_button_unchecked,
                          size: 16,
                          color: (stage['done'] == true) ? Colors.green : Colors.grey,
                        ),
                        const SizedBox(width: 6),
                        Text(stage['stage'].toString()),
                      ],
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }

  String _label(String key) {
    return key
        .split('_')
        .map((w) => w.isEmpty ? w : w[0].toUpperCase() + w.substring(1))
        .join(' ');
  }
}
