import { useSupabase } from "@/app/supabase-provider";
import axios from "axios";
import { redirect } from "next/navigation";
import { useCallback, useRef, useState } from "react";
import { useToast } from "../../../hooks/useToast";
import { isValidUrl } from "../helpers/isValidUrl";

export const useCrawler = () => {
  const [isCrawling, setCrawling] = useState(false);
  const urlInputRef = useRef<HTMLInputElement | null>(null);
  const { setMessage, messageToast } = useToast();
  const { session } = useSupabase();
  if (session === null) {
    redirect("/login");
  }

  const crawlWebsite = useCallback(async () => {
    setCrawling(true);
    // Validate URL
    const url = urlInputRef.current ? urlInputRef.current.value : null;

    if (!url || !isValidUrl(url)) {
      // Assuming you have a function to validate URLs
      setMessage({
        type: "error",
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
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/crawl`,
        config,
        {
          headers: {
            Authorization: `Bearer ${session.access_token}`,
          },
        }
      );

      setMessage({
        type: response.data.type,
        text: response.data.message,
      });
    } catch (error: unknown) {
      setMessage({
        type: "error",
        text: "Failed to crawl website: " + JSON.stringify(error),
      });
    } finally {
      setCrawling(false);
    }
  }, [session.access_token]);

  return {
    isCrawling,
    urlInputRef,
    messageToast,
    crawlWebsite,
  };
};
