import 'package:flutter/material.dart';

/// Renders the `flight_page` ui_type — list of flight options. Mirrors
/// HotelWidget's structure for visual consistency across travel results.
class FlightWidget extends StatelessWidget {
  final Map<String, dynamic> data;

  const FlightWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final flights = (data['flights'] as List<dynamic>?) ?? const [];

    if (flights.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(16.0),
        child: Text('No flights found.'),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      padding: const EdgeInsets.symmetric(vertical: 8),
      itemCount: flights.length,
      itemBuilder: (context, index) {
        final flight = flights[index] as Map<String, dynamic>;
        return Card(
          margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          elevation: 2,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: ListTile(
            leading: const Icon(Icons.flight, color: Colors.indigo),
            title: Text(flight['airline']?.toString() ?? 'Unknown airline'),
            subtitle: Text('${flight['route'] ?? ''} · ${flight['duration'] ?? ''}'),
            trailing: Text(
              flight['price']?.toString() ?? '-',
              style: TextStyle(color: Colors.green.shade700, fontWeight: FontWeight.w600),
            ),
          ),
        );
      },
    );
  }
}
