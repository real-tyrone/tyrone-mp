# negotiated integration AI journal participation

Added `common/on_actions/chi_adm_negotiated_integration_ai.txt`:

- AI China with the combined administrations JE proposes integration to one eligible administration each month.
- Uses the player's existing eligibility and proposal effects, including Autonomy, technology, centralization, resources, peace and cooldown checks.
- Revisits one pending provincial reply each month through the existing court event and its AI response weights.
- Provincial acceptance, concessions, player consent and annexation still use existing negotiated integration events and effects.

Validation: existing negotiated integration static checks pass. The behavioral validator currently stops at its legacy fiscal-state timer assertion (`chi_adm_negotiated_integration_tax_left`); it therefore does not establish a full behavioral pass. Runtime observation remains required for monthly AI proposals, replies, resource gating and completed annexation.
