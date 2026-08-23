/** Tipos das respostas da API Clinicorp (validados contra dados reais no Dash-Unidades-BS). */

/**
 * Item do ProcedureList de um orcamento.
 *
 * ATENCAO: ao contrario do que a doc sugere, este objeto NAO traz ProcedureName.
 * O nome do procedimento sai do catalogo (/procedures/list), casando
 * PriceId (aqui) com id (la). Verificado contra a API em 08/2026.
 */
export interface ClinicorpProcedure {
  PriceId?: number;
  Procedure_CharacteristicId?: number;
  PriceListId?: number;
  Amount: number;
  FinalAmount?: number;
  OriginalAmount?: number;
  Executed?: string; // "X" | ""
  Tooth?: string;
  Surface?: string;
  HasSteps?: string;
  /** Presente em algumas contas; nao confie nele. */
  ProcedureName?: string;
  ProcedureExpertiseName?: string;
}

export interface ClinicorpEstimateStep {
  StepDescription: string;
  Executed: string; // "X" | ""
  ExecutedDate: string | null;
  ProfessionalName: string;
}

export interface ClinicorpEstimate {
  id: number;
  TreatmentId: number;
  PatientName: string;
  PatientId: number;
  PatientMobilePhone?: string;
  Amount: number;
  Status: "APPROVED" | "OPEN" | "FOLLOW_UP" | "REJECTED" | string;
  CreateDate: string;
  BusinessId: number;
  ProfessionalId: number;
  ProfessionalName: string;
  DiscountPercentage?: number;
  ProcedureList?: ClinicorpProcedure[];
  StepsList?: ClinicorpEstimateStep[];
}

export interface ClinicorpPayment {
  id: number;
  PaymentHeaderId: number;
  PatientName: string;
  PatientId: number;
  Amount: number;
  PaymentForm: string;
  Type: string;
  CreditDebitCardFlag?: string;
  InstallmentsCount: number;
  InstallmentNumber: number;
  TotalPostAmount?: number;
  DueDate: string;
  CheckOutDate: string;
  PaymentReceived: string; // "X" | ""
  PaymentConfirmed: string; // "X" | ""
  TreatmentId: number;
  Last4Digits?: string;
  AmountWithDiscounts?: number;
  OwnerName?: string;
  AuthorizationCode?: string;
}
