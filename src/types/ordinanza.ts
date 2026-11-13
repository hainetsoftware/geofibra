export type Ente = "COMUNE_COLLESALVETTI" | "PROVINCIA_LIVORNO";
export type Settore = "POLIZIA_LOCALE" | "LAVORI_PUBBLICI" | "PATRIMONIO_TRIBUTI" | "STRATEGICO";
export type Tipologia = "ORDINANZA_VIABILITA" | "CONCESSIONE_SUOLO" | "AUTORIZZAZIONE_SCAVO" |
    "PROROGA" | "RIPRISTINO" | "ALTRO";
export type Area = "COLLESALVETTI" | "STAGNO" | "VICARELLO" | "GUASTICCE" | "NUGOLA" | "EXTRAURBANO";
export type Operatore = "FiberCop" | "Fastweb" | "TIM" | "Open Fiber" | "WindTre" | "Estracom" | "Ultranet" | "Altri";
export type StatoOpera = "PROGRAMMATA" | "IN_CORSO" | "COMPLETATA" | "DECADUTA";
export type StatoAtto = "PROGRAMMATA" | "IN_CORSO" | "TERMINATA" | "NON_DOCUMENTATA";

export interface RiferimentoAtto {
    tipo: "AUTORIZZAZIONE" | "ORDINANZA" | "CONCESSIONE";
    numero: string;
    data: string | null;
    ente: Ente | null;
    atto_id?: string;
}

export interface OrdinanzaAtto {
    id: string;
    ente: Ente | null;
    settore: Settore | null;
    funzionario: string | null;
    tipologia: Tipologia;
    numero_atto: string | null;
    registro_generale: string | null;
    protocollo: string | null;
    data_emissione: string | null;
    data_registrazione: string | null;
    data_protocollo: string | null;
    cluster_id?: string;
    oggetto: string | null;
    richiedente: string | null;
    operator_target: Operatore | null;
    validita: { dal: string | null; al: string | null; orario: string | null; periodi?: { dal: string; al: string }[] };
    localizzazione: {
        area: Area | null;
        strade: string[];
        prog_chilometrica: { dal_km: number; al_km: number } | null;
        matched_feature_ids: string[];
        candidate_feature_ids: string[];
    };
    file_pdf: { nome_file: string; url_path: string };
    riferimenti: RiferimentoAtto[];
    atti_collegati: string[];
    note_tecniche?: string;
    ocr_required: boolean;
    stato_opera: StatoOpera | null;
}

declare global {
    interface Window {
        ARCHIVIO_ATTI?: OrdinanzaAtto[];
        ARCHIVIO_TESTI?: Record<string, string>;
        appendArchivioLinks?: (element: HTMLElement, featureId: string, options?: { includePdf?: boolean }) => Promise<void>;
        showArchivioFeatures?: (ids: string[], originFeatureId?: string) => void;
    }
}
