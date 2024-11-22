from flask import jsonify

class ZakatService:
    def calculate_zakat(self, total_assets, total_liabilities):
        """Calculate Zakat based on total assets and liabilities."""
        if total_assets < total_liabilities:
            return jsonify({'error': 'Liabilities exceed assets, Zakat cannot be calculated.'}), 400
        
        net_assets = total_assets - total_liabilities
        zakat_due = net_assets * 0.025  # 2.5% Zakat rate
        
        return jsonify({
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'net_assets': net_assets,
            'zakat_due': zakat_due
        }), 200

    def get_zakat_details(self, user_id):
        """Retrieve Zakat details for a user (placeholder for future implementation)."""
        # This method can be expanded to fetch user-specific Zakat details from a database
        return jsonify({'message': 'Zakat details retrieval is not yet implemented for this user.'}), 501

    def validate_assets_liabilities(self, assets, liabilities):
        """Validate the assets and liabilities input."""
        if not isinstance(assets, (int, float)) or not isinstance(liabilities, (int, float)):
            return jsonify({'error': 'Assets and liabilities must be numeric values.'}), 400
        if assets < 0 or liabilities < 0:
            return jsonify({'error': 'Assets and liabilities must be non-negative.'}), 400
        return True

    def calculate_zakat_for_user(self, user_id, assets, liabilities):
        """Calculate Zakat for a specific user."""
        validation = self.validate_assets_liabilities(assets, liabilities)
        if validation is not True:
            return validation
        
        return self.calculate_zakat(assets, liabilities)
