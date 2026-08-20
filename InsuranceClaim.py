from datetime import datetime, timedelta


class InsuranceClaim:
    def __init__(self):

        self.coverage_limits = {
            "Health": 500000,
            "Vehicle": 300000,
            "Life": 1000000,
            "Travel": 200000
        }

    def validate_policy_number(
        self,
        policy_number
    ):
        if (
            not policy_number
            or
            not policy_number.startswith("POL")
        ):
            raise ValueError(
                "Invalid policy number"
            )

    def process_claim(
        self,
        policy_number,
        customer_id,
        policy_type,
        claim_amount,
        policy_start_date,
        incident_date,
        previous_claim_count,
        customer_age,
        incident_type,
        documents_available
    ):
        self.validate_policy_number(
            policy_number
        )

        if policy_type not in self.coverage_limits:
            raise ValueError(
                "Invalid policy type"
            )

        if claim_amount <= 0:
            raise ValueError(
                "Invalid claim amount"
            )

        if customer_age < 0:
            raise ValueError(
                "Invalid customer age"
            )

        if isinstance(policy_start_date, str):
            policy_start_date = datetime.strptime(
                policy_start_date,
                "%Y-%m-%d"
            )

        if isinstance(incident_date, str):
            incident_date = datetime.strptime(
                incident_date,
                "%Y-%m-%d"
            )

        policy_expiry = (
            policy_start_date
            + timedelta(days=365)
        )

        coverage = self.coverage_limits[
            policy_type
        ]

        if incident_date < policy_start_date:
            return self.create_result(
                "REJECTED",
                0,
                0,
                0,
                0,
                "Incident occurred before policy start"
            )

        if incident_date > policy_expiry:
            return self.create_result(
                "REJECTED",
                0,
                0,
                0,
                0,
                "Policy expired"
            )

        fraud_score = 0
        fraud_reasons = []

        days_after_activation = (
            incident_date
            - policy_start_date
        ).days

        if previous_claim_count >= 3:
            fraud_score += 2
            fraud_reasons.append(
                "Multiple previous claims"
            )

        elif previous_claim_count > 0:
            fraud_score += 1

        if claim_amount > coverage:
            fraud_score += 2
            fraud_reasons.append(
                "Claim exceeds policy coverage"
            )

        if days_after_activation <= 7:
            fraud_score += 2
            fraud_reasons.append(
                "Incident shortly after policy activation"
            )

        if not documents_available:
            fraud_score += 1
            fraud_reasons.append(
                "Missing documentation"
            )

        maximum_payable = min(
            claim_amount,
            coverage
        )

        deductible = (
            maximum_payable * 0.10
        )

        customer_contribution = deductible

        insurance_payout = (
            maximum_payable
            - deductible
        )

        if fraud_score >= 4:
            status = "FRAUD SUSPECTED"

        elif not documents_available:
            status = "MANUAL REVIEW"

        elif fraud_score >= 2:
            status = "MANUAL REVIEW"

        else:
            status = "APPROVED"

        return self.create_result(
            status,
            maximum_payable,
            deductible,
            customer_contribution,
            insurance_payout,
            ", ".join(fraud_reasons),
            fraud_score
        )

    def create_result(
        self,
        status,
        maximum_payable,
        deductible,
        customer_contribution,
        payout,
        reason="",
        fraud_score=0
    ):
        return {
            "status": status,
            "maximum_payable": round(
                maximum_payable,
                2
            ),
            "deductible": round(
                deductible,
                2
            ),
            "customer_contribution": round(
                customer_contribution,
                2
            ),
            "insurance_payout": round(
                payout,
                2
            ),
            "fraud_score": fraud_score,
            "reason": reason
        }


if __name__ == "__main__":
    system = InsuranceClaim()

    result = system.process_claim(
        "POL1001",
        "C101",
        "Health",
        100000,
        "2026-01-01",
        "2026-05-10",
        0,
        30,
        "Hospitalization",
        True
    )

    print(result)
