/** Tipos das respostas da API Clinicorp (validados contra dados reais no Dash-Unidades-BS). */

export interface ClinicorpProcedure {
  ProcedureName: string;
  ProcedureExpertiseName: string;
  OriginalAmount: number;
  OperationDescription: string;
  Amount: number;
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
