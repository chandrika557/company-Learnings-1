Convert the RAML into equivalent C# Models and DTOs.

Guidelines:
- Undrstand current dot net core web api solution Architecture 
- Use strongly typed Models, DTOs, Enums
- Handle null safety based on existing standards

One-shot example:
RAML map → Models & DTO
RAML:
  ## 4. Response Data Type Definition

#%RAML 1.0 DataType
description: Results from WSBND Method Call for Request Option(N)
properties:
  effective_date:
    description: Maps to DT_EFFECT
    type: date-only
  bond_form_type?:
    description: Maps to FORM_DESC
    type: string
  form_number?:
    description: Maps to NO_FORM
    type: string
  bond_state:
    description: Maps to PREM_ST
    type: string
  bond_zip:
    description: Maps to PRM_ZIP
    type: string
  bond_description:
    description: Maps to DESC_PROJ
    type: string
  obligee_name:
    description: Maps to OBLG_NM 
    type: string
  obligee_street_address:
    description: Maps to OBLG_ADDR
    type: string
  obligee_street_address2?:
    description: Maps to OBLG_ADDR2
    type: string
  obligee_city_state_zip?:
    description: Maps to OBLG_CSZ
    type: string
  obligee_phone:
    description: Maps to OBLG_PHONE
    type: string
  maintenance_bond?:
    description: Maps to YON_MAINT
    type: boolean
  maintenance_period?:
    description: Maps to YRS_MAINT
    type: string 
  contract_date?:
    description: Maps to DT_CONTR
    type: string
  contract_amount?:
    description: Maps to AMT_CONTR
    type: string
  bond_premium?:
    description: Maps to PRM_TOTAL
    type: string
  bid_date?:
    description: Maps to DT_BIDDUE
    type: date-only
  bid_percent?:
    description: Maps to AMT_PERCNT
    type: string
  bid_amount:
    description: Maps to AMT_BID
    type: string
  account_number?:
    description: Maps to ACCOUNT_NO
    type: string
  account_name?:
    description: Maps to ACCT_NM
    type: string
  account_street_address?:
    description: Maps to ACCT_ADDR
    type: string
  account_city?:
    description: Maps to ACCT_CITY
    type: string
  account_state?:
    description: Maps to ACCT_ST
    type: string
  account_zip?:
    description: Maps to ACCT_ZIP
    type: string
  agency_number?:
    description: Maps to AGENT_NO
    type: string
  producer_number?:
    description: Maps to NO_SUBPROD
    type: string
  bond_type?:
    description: Maps to BOND_TYPE
    type: string
  completion_date:
    description: Maps to DT_COMPL
    type: date-only
  is_renewable_after_year:
    description: Maps to YON_RNW1YR
    type: boolean
  liquidated_damages?:
    description: Maps to AMT_DAMAGE
    type: string
  second_lowest_bidder?:
    description: Maps to AMT_LOWBD2
    type: string
  bid_estimate?:
    description: Maps to AMT_BIDEST
    type: string
  type_of_bond: 
    type: string
    example: 'Performance'
  #bond_status_short is currently a flag only used by bonds system.
  bond_status_short:
    description: Maps to STS_FILE 
    type: string
  #bond_status will give us actual status of bond. IE: OPEN, LAPSED etc.
  bond_status:
    description: Maps to bond_status (from WSINQ - this gives us bond status)
    type: string
    


Models, DTOs, Enums output:
---
Model Class:
   [SwaggerSchema("Comprehensive bond information for the Underwriter Review Screen, aggregated from WSBND and WSQAP systems")]
public class UnderwriterInformationResponse
{
	[JsonPropertyName("effective_date")]
	public DateOnly? EffectiveDate { get; set; }

	[JsonPropertyName("bond_form_type")]
	public string? BondFormType { get; set; }

	[JsonPropertyName("form_number")]
	public string? FormNumber { get; set; }

	[JsonPropertyName("bond_state")]
	public string? BondState { get; set; }

	[JsonPropertyName("bond_zip")]
	public string? BondZip { get; set; }

	[JsonPropertyName("bond_description")]
	public string? BondDescription { get; set; }

	[JsonPropertyName("obligee_name")]
	public string? ObligeeName { get; set; }

	[JsonPropertyName("obligee_street_address")]
	public string? ObligeeStreetAddress { get; set; }

	[JsonPropertyName("obligee_street_address2")]
	public string? ObligeeStreetAddress2 { get; set; }

	[JsonPropertyName("obligee_city_state_zip")]
	public string? ObligeeCityStateZip { get; set; }

	[JsonPropertyName("obligee_phone")]
	public string? ObligeePhone { get; set; }

	[JsonPropertyName("maintenance_bond")]
	public bool? MaintenanceBond { get; set; }

	[JsonPropertyName("maintenance_period")]
	public string? MaintenancePeriod { get; set; }

	[JsonPropertyName("contract_date")]
	public DateOnly? ContractDate { get; set; }

	[JsonPropertyName("contract_amount")]
	public decimal? ContractAmount { get; set; }

	[JsonPropertyName("bond_premium")]
	public decimal? BondPremium { get; set; }

	[JsonPropertyName("bid_date")]
	public DateOnly? BidDate { get; set; }

	[JsonPropertyName("bid_percent")]
	public string? BidPercent { get; set; }

	[JsonPropertyName("bid_amount")]
	public decimal? BidAmount { get; set; }

	[JsonPropertyName("account_number")]
	public string? AccountNumber { get; set; }

	[JsonPropertyName("account_name")]
	public string? AccountName { get; set; }

	[JsonPropertyName("account_street_address")]
	public string? AccountStreetAddress { get; set; }

	[JsonPropertyName("account_city")]
	public string? AccountCity { get; set; }

	[JsonPropertyName("account_state")]
	public string? AccountState { get; set; }

	[JsonPropertyName("account_zip")]
	public string? AccountZip { get; set; }

	[JsonPropertyName("agency_number")]
	public string? AgencyNumber { get; set; }

	[JsonPropertyName("producer_number")]
	public string? ProducerNumber { get; set; }

	[JsonPropertyName("bond_type")]
	public string? BondType { get; set; }

	[JsonPropertyName("completion_date")]
	public DateOnly? CompletionDate { get; set; }

	[JsonPropertyName("is_renewable_after_year")]
	public bool? IsRenewableAfterYear { get; set; }

	[JsonPropertyName("liquidated_damages")]
	public string? LiquidatedDamages { get; set; }

	[JsonPropertyName("second_lowest_bidder")]
	public string? SecondLowestBidder { get; set; }

	[JsonPropertyName("bid_estimate")]
	public string? BidEstimate { get; set; }

	[JsonPropertyName("type_of_bond")]
	public string? TypeOfBond { get; set; }

	[JsonPropertyName("bond_city")]
	public string? BondCity { get; set; }

	[JsonPropertyName("bond_status_short")]
	public string? BondStatusShort { get; set; }

	[JsonPropertyName("bond_status")]
	public string? BondStatus { get; set; }
}

Enum: 

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum BondStatusEnum
{
	[Description("Open")]
	X,

	[Description("Closed")]
	C,

	[Description("Cancelled")]
	N,

	[Description("Pending")]
	P,

	[Description("Issued")]
	I
}