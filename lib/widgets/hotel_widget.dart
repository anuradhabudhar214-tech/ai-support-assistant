import 'package:flutter/material.dart';

/// Renders the `hotel_page` ui_type with a real, structured UI: a scrollable
/// list of Cards, each showing a placeholder image, name, price, and rating
/// — per the spec's HotelWidget requirement.
class HotelWidget extends StatelessWidget {
  final Map<String, dynamic> data;

  const HotelWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final hotels = (data['hotels'] as List<dynamic>?) ?? const [];

    if (hotels.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(16.0),
        child: Text('No hotels found.'),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      padding: const EdgeInsets.symmetric(vertical: 8),
      itemCount: hotels.length,
      itemBuilder: (context, index) {
        final hotel = hotels[index] as Map<String, dynamic>;
        final name = hotel['name']?.toString() ?? 'Unknown hotel';
        final price = hotel['price']?.toString() ?? '-';
        final rating = hotel['rating'];

        return Card(
          margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          elevation: 2,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: Padding(
            padding: const EdgeInsets.all(12.0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Image placeholder, as required by the spec.
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    width: 64,
                    height: 64,
                    color: Colors.blueGrey.shade100,
                    child: const Icon(Icons.hotel, size: 32, color: Colors.blueGrey),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        name,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          Text(
                            price,
                            style: TextStyle(
                              color: Colors.green.shade700,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(width: 12),
                          if (rating != null) ...[
                            const Icon(Icons.star, size: 16, color: Colors.amber),
                            const SizedBox(width: 2),
                            Text(rating.toString()),
                          ],
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
