import { useSupabase } from "@/app/supabase-provider";
import { useToast } from "@/lib/hooks/useToast";
import { useAxios } from "@/lib/useAxios";
import axios, { AxiosError } from "axios";
import { redirect } from "next/navigation";
import { useCallback, useRef, useState } from "react";
import { isValidUrl } from "../helpers/isValidUrl";

interface ErrorData {
  message?: string;
}

export const useCrawler = () => {
  const [isCrawling, setCrawling] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const urlInputRef = useRef<HTMLInputElement | null>(null);
  const { session } = useSupabase();
  const { publish } = useToast();
  const { axiosInstance } = useAxios();

  if (session === null) {
    redirect("/login");
  }

  const logErrorToBackend = async (errorMessage: string): Promise<void> => {
    await axios.post("/logerror", { message: errorMessage });
  };

  const crawlWebsite = useCallback(async () => {
    setCrawling(true);
    // Validate URL
    const url = urlInputRef.current ? urlInputRef.current.value : null;

    if (!url || !isValidUrl(url)) {
      // Assuming you have a function to validate URLs
      publish({
        variant: "danger",
        text: "Invalid URL",
      });
      setCrawling(false);
      return;
    }

    // Configure parameters
    const config = {
      url: url,
      js: false,
      depth: 1,
      max_pages: 100,
      max_time: 60,
    };

    try {
      const response = await axiosInstance.post(`/crawl`, config);

      publish({
        variant: response.data.type,
        text: response.data.message,
      });
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError;
        // Extract and log detailed information about the error
        console.log("Axios request configuration:", axiosError.config);
        console.log("Request made:", axiosError.request);
        console.log("Server response:", axiosError.response);

        if (axiosError.response && axiosError.response.data) {
          // If the server response includes a data object, use that as the error message
          const errorData = axiosError.response.data as ErrorData;
          setErrorMessage(errorData.message || "Unknown error");
        } else {
          // Otherwise, use the error message from the AxiosError object
          setErrorMessage(axiosError.message);
        }

        // Log the error message to the backend
        if (errorMessage) {
          await logErrorToBackend(errorMessage);
        }
        
        publish({
          variant: "danger",
          text: "Failed to crawl website: " + errorMessage,
        });
      } else {
        // If the error isn't an AxiosError, it might have a message property
        setErrorMessage((error as Error).message);
      }
    } finally {
      setCrawling(false);
    }
  }, [session.access_token, publish]);

  return {
    isCrawling,
    urlInputRef,
    crawlWebsite,
    errorMessage,
  };
};
