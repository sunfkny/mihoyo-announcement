/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** Bh3GachaInfo */
export interface Bh3GachaInfo {
  /** Ann Id */
  ann_id: number;
  /** Title */
  title: string;
  /** Image */
  image: string;
  /** Content */
  content: string;
  /** Info Html */
  info_html: string | null;
}

/** Bh3Progress */
export interface Bh3Progress {
  /** Text */
  text: string | null;
  /** Percent */
  percent: number | null;
}

/** Bh3Response */
export interface Bh3Response {
  progress: Bh3Progress;
  /** Gacha Info */
  gacha_info: Bh3GachaInfo[];
}

/** Hk4eGachaInfo */
export interface Hk4EGachaInfo {
  /** Ann Id */
  ann_id: number;
  /** Title */
  title: string;
  /** Image */
  image: string;
  /** Content */
  content: string;
  /** Start Time */
  start_time: string | null;
  /** End Time */
  end_time: string | null;
}

/** Hk4eProgress */
export interface Hk4EProgress {
  /** Text */
  text: string | null;
  /** Percent */
  percent: number | null;
}

/** Hk4eResponse */
export interface Hk4EResponse {
  progress: Hk4EProgress;
  /** Gacha Info */
  gacha_info: Hk4EGachaInfo[];
}

/** HkrpgGachaInfo */
export interface HkrpgGachaInfo {
  /** Ann Id */
  ann_id: number;
  /** Title */
  title: string;
  /** Image */
  image: string;
  /** Content */
  content: string;
  /** Start Time */
  start_time: string | null;
  /** End Time */
  end_time: string | null;
}

/** HkrpgProgress */
export interface HkrpgProgress {
  /** Text */
  text: string | null;
  /** Percent */
  percent: number | null;
}

/** HkrpgResponse */
export interface HkrpgResponse {
  progress: HkrpgProgress;
  /** Gacha Info */
  gacha_info: HkrpgGachaInfo[];
}

/** NapGachaInfo */
export interface NapGachaInfo {
  /** Ann Id */
  ann_id: number;
  /** Title */
  title: string;
  /** Image */
  image: string;
  /** Content */
  content: string;
  /** Start Time */
  start_time: string | null;
  /** End Time */
  end_time: string | null;
}

/** NapProgress */
export interface NapProgress {
  /** Text */
  text: string | null;
  /** Percent */
  percent: number | null;
}

/** NapResponse */
export interface NapResponse {
  progress: NapProgress;
  /** Gacha Info */
  gacha_info: NapGachaInfo[];
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, "body" | "method" | "query" | "path">;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (securityData: SecurityDataType | null) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter((key) => "undefined" !== typeof query[key]);
    return keys
      .map((key) => (Array.isArray(query[key]) ? this.addArrayQueryParam(query, key) : this.addQueryParam(query, key)))
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string") ? JSON.stringify(input) : input,
    [ContentType.Text]: (input: any) => (input !== null && typeof input !== "string" ? JSON.stringify(input) : input),
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(`${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`, {
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type && type !== ContentType.FormData ? { "Content-Type": type } : {}),
      },
      signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
      body: typeof body === "undefined" || body === null ? null : payloadFormatter(body),
    }).then(async (response) => {
      const r = response.clone() as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title FastAPI
 * @version 0.1.0
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  api = {
    /**
     * No description
     *
     * @name ApiBh3ApiBh3Get
     * @summary Api Bh3
     * @request GET:/api/bh3
     */
    apiBh3ApiBh3Get: (params: RequestParams = {}) =>
      this.request<Bh3Response, any>({
        path: `/api/bh3`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @name ApiHk4EApiHk4EGet
     * @summary Api Hk4E
     * @request GET:/api/hk4e
     */
    apiHk4EApiHk4EGet: (params: RequestParams = {}) =>
      this.request<Hk4EResponse, any>({
        path: `/api/hk4e`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @name ApiHkrpgApiHkrpgGet
     * @summary Api Hkrpg
     * @request GET:/api/hkrpg
     */
    apiHkrpgApiHkrpgGet: (params: RequestParams = {}) =>
      this.request<HkrpgResponse, any>({
        path: `/api/hkrpg`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @name ApiNapApiNapGet
     * @summary Api Nap
     * @request GET:/api/nap
     */
    apiNapApiNapGet: (params: RequestParams = {}) =>
      this.request<NapResponse, any>({
        path: `/api/nap`,
        method: "GET",
        format: "json",
        ...params,
      }),
  };
}
