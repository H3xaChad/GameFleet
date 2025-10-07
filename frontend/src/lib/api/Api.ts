/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** ServerStatus */
export enum ServerStatus {
  Online = "online",
  Offline = "offline",
  Unknown = "unknown",
}

/** GameServerType */
export enum GameServerType {
  Minecraft = "minecraft",
  Factorio = "factorio",
  Satisfactory = "satisfactory",
  ArkAse = "ark_ase",
  ArkAsa = "ark_asa",
  Valheim = "valheim",
}

/**
 * BaseServerInfo
 * Base model for live server information that all game servers should provide.
 */
export interface BaseServerInfo {
  status: ServerStatus;
  /** Latency */
  latency?: number | null;
  /** Version */
  version?: string | null;
  /** Description */
  description?: string | null;
  /** Icon */
  icon?: string | null;
  /** Mods */
  mods?: Record<string, any>[] | null;
  /** Game Mode */
  game_mode?: string | null;
  /** Map Name */
  map_name?: string | null;
  /** Password Protected */
  password_protected?: boolean | null;
  /** Anti Cheat Enabled */
  anti_cheat_enabled?: boolean | null;
  /** Players Online */
  players_online?: number | null;
  /** Players Max */
  players_max?: number | null;
  /** Player List */
  player_list?: string[] | null;
  /** Error Message */
  error_message?: string | null;
}

/** GameServer */
export interface GameServer {
  /** Id */
  id?: string;
  game: GameServerType;
  /**
   * Name
   * @maxLength 100
   */
  name: string;
  /**
   * Address
   * @maxLength 100
   */
  address: string;
  /**
   * Port
   * @min 1
   * @max 65535
   */
  port: number;
}

/** GameServerCreate */
export interface GameServerCreate {
  /** Name */
  name: string;
  game: GameServerType;
  /** Address */
  address: string;
  /** Port */
  port: number;
}

/** GameServerUpdate */
export interface GameServerUpdate {
  /** Name */
  name?: string | null;
  game?: GameServerType | null;
  /** Address */
  address?: string | null;
  /** Port */
  port?: number | null;
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
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

export type RequestParams = Omit<
  FullRequestParams,
  "body" | "method" | "query" | "path"
>;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (
    securityData: SecurityDataType | null,
  ) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown>
  extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  JsonApi = "application/vnd.api+json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) =>
    fetch(...fetchParams);

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
    const keys = Object.keys(query).filter(
      (key) => "undefined" !== typeof query[key],
    );
    return keys
      .map((key) =>
        Array.isArray(query[key])
          ? this.addArrayQueryParam(query, key)
          : this.addQueryParam(query, key),
      )
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string")
        ? JSON.stringify(input)
        : input,
    [ContentType.JsonApi]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string")
        ? JSON.stringify(input)
        : input,
    [ContentType.Text]: (input: any) =>
      input !== null && typeof input !== "string"
        ? JSON.stringify(input)
        : input,
    [ContentType.FormData]: (input: any) => {
      if (input instanceof FormData) {
        return input;
      }

      return Object.keys(input || {}).reduce((formData, key) => {
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
      }, new FormData());
    },
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(
    params1: RequestParams,
    params2?: RequestParams,
  ): RequestParams {
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

  protected createAbortSignal = (
    cancelToken: CancelToken,
  ): AbortSignal | undefined => {
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

    return this.customFetch(
      `${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`,
      {
        ...requestParams,
        headers: {
          ...(requestParams.headers || {}),
          ...(type && type !== ContentType.FormData
            ? { "Content-Type": type }
            : {}),
        },
        signal:
          (cancelToken
            ? this.createAbortSignal(cancelToken)
            : requestParams.signal) || null,
        body:
          typeof body === "undefined" || body === null
            ? null
            : payloadFormatter(body),
      },
    ).then(async (response) => {
      const r = response as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const responseToParse = responseFormat ? response.clone() : response;
      const data = !responseFormat
        ? r
        : await responseToParse[responseFormat]()
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
 * @title Game Server Dashboard API
 * @version 0.1.0
 *
 * API for managing and monitoring game servers
 */
export class Api<
  SecurityDataType extends unknown,
> extends HttpClient<SecurityDataType> {
  /**
   * No description
   *
   * @name RootGet
   * @summary Root
   * @request GET:/
   */
  rootGet = (params: RequestParams = {}) =>
    this.request<any, any>({
      path: `/`,
      method: "GET",
      format: "json",
      ...params,
    });

  api = {
    /**
     * @description Get all game servers from the database.
     *
     * @tags servers
     * @name GetServersApiServersGet
     * @summary Get Servers
     * @request GET:/api/servers
     */
    getServersApiServersGet: (params: RequestParams = {}) =>
      this.request<GameServer[], any>({
        path: `/api/servers`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags servers
     * @name CreateServerApiServersPost
     * @summary Create Server
     * @request POST:/api/servers
     */
    createServerApiServersPost: (
      data: GameServerCreate,
      params: RequestParams = {},
    ) =>
      this.request<GameServer, HTTPValidationError>({
        path: `/api/servers`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags servers
     * @name GetServerApiServersServerIdGet
     * @summary Get Server
     * @request GET:/api/servers/{server_id}
     */
    getServerApiServersServerIdGet: (
      serverId: string,
      params: RequestParams = {},
    ) =>
      this.request<GameServer, HTTPValidationError>({
        path: `/api/servers/${serverId}`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags servers
     * @name UpdateServerApiServersServerIdPut
     * @summary Update Server
     * @request PUT:/api/servers/{server_id}
     */
    updateServerApiServersServerIdPut: (
      serverId: string,
      data: GameServerUpdate,
      params: RequestParams = {},
    ) =>
      this.request<GameServer, HTTPValidationError>({
        path: `/api/servers/${serverId}`,
        method: "PUT",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Delete a game server.
     *
     * @tags servers
     * @name DeleteServerApiServersServerIdDelete
     * @summary Delete Server
     * @request DELETE:/api/servers/{server_id}
     */
    deleteServerApiServersServerIdDelete: (
      serverId: string,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/api/servers/${serverId}`,
        method: "DELETE",
        format: "json",
        ...params,
      }),

    /**
     * @description Get all servers of a specific game type.
     *
     * @tags servers
     * @name GetServersByTypeApiServersByTypeServerTypeGet
     * @summary Get Servers By Type
     * @request GET:/api/servers/by-type/{server_type}
     */
    getServersByTypeApiServersByTypeServerTypeGet: (
      serverType: GameServerType,
      params: RequestParams = {},
    ) =>
      this.request<GameServer[], HTTPValidationError>({
        path: `/api/servers/by-type/${serverType}`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description Get live information for a server by its database ID.
     *
     * @tags servers
     * @name GetServerLiveInfoByIdApiServersServerIdLiveInfoGet
     * @summary Get Server Live Info By Id
     * @request GET:/api/servers/{server_id}/live-info
     */
    getServerLiveInfoByIdApiServersServerIdLiveInfoGet: (
      serverId: string,
      params: RequestParams = {},
    ) =>
      this.request<BaseServerInfo, HTTPValidationError>({
        path: `/api/servers/${serverId}/live-info`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description Get list of supported game server types.
     *
     * @tags servers
     * @name SupportedTypesApiServersSupportedTypesGet
     * @summary Supported Types
     * @request GET:/api/servers/supported_types
     */
    supportedTypesApiServersSupportedTypesGet: (params: RequestParams = {}) =>
      this.request<GameServerType[], any>({
        path: `/api/servers/supported_types`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags docker
     * @name ListContainersApiDockerContainersGet
     * @summary List Containers
     * @request GET:/api/docker/containers
     */
    listContainersApiDockerContainersGet: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/api/docker/containers`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags docker
     * @name StartContainerApiDockerStartContainerIdPost
     * @summary Start Container
     * @request POST:/api/docker/start/{container_id}
     */
    startContainerApiDockerStartContainerIdPost: (
      containerId: string,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/api/docker/start/${containerId}`,
        method: "POST",
        format: "json",
        ...params,
      }),
  };
}
