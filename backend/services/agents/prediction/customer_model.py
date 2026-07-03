from typing import List


class CustomerModel:
    def __init__(self, churn_rate: float, acquisition_rate: float):
        self.churn_rate = churn_rate
        self.acquisition_rate = acquisition_rate

    def project_customers(self, current_customers: int, periods: int) -> List[int]:
        customers = []
        current = current_customers
        for _ in range(periods):
            new_customers = int(current * self.acquisition_rate)
            churned = int(current * self.churn_rate)
            current = current + new_customers - churned
            customers.append(current)
        return customers
