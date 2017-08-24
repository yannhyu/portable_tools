SELECT 
  id_rec,
  dataload->>'cpi' as cpi,
  dataload->>'acctnum' as acctnum,
  dataload->>'charges' as charges,
  dataload->>'balance' as balance
FROM unstaged_tbl
WHERE dataload->>'cpi' = 'E1503798226'
AND dataload->>'acctnum' = '58000019305';

----
UPDATE unstaged_tbl
SET dataload=jsonb_set(dataload, '{balance}', '"(1,609.02)"', true) 
WHERE dataload->>'cpi' = 'E1503798226'
AND dataload->>'acctnum' = '58000019305';
--where dataload is a jsonb column type.
