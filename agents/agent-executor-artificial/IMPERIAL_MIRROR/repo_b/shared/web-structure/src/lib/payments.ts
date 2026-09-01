/**
 * Standard Payment Integration Utility
 * Supports Kiwify and Hotmart link generation with UTM tracking.
 */

export interface TrackingParams {
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_content?: string;
  utm_term?: string;
  src?: string; // Standard Hotmart/Kiwify 'src' param
}

export const getCheckoutUrl = (baseUrl: string, params: TrackingParams = {}): string => {
  try {
    const url = new URL(baseUrl);
    Object.entries(params).forEach(([key, value]) => {
      if (value) url.searchParams.append(key, value);
    });
    return url.toString();
  } catch (e) {
    console.error("Invalid checkout base URL", baseUrl);
    return baseUrl;
  }
};

export const KIWIFY_DEFAULT_CHECKOUT = "https://pay.kiwify.com.br/placeholder";
export const HOTMART_DEFAULT_CHECKOUT = "https://pay.hotmart.com/placeholder";
