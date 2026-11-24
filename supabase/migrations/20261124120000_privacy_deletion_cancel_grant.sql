-- SYNTRA Social 2.34.1
-- Allow an authenticated account to cancel its own pending deletion request.
-- RLS policies still restrict the row to auth.uid() = user_id and status = 'pending'.
-- Column-level privilege prevents clients from changing user_id or other request metadata.

GRANT UPDATE (status) ON TABLE public.account_deletion_requests TO authenticated;
