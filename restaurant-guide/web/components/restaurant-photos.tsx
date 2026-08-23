"use client";

import {
  createContext,
  useContext,
  useEffect,
  useId,
  useMemo,
  useState,
} from "react";
import { CameraMark } from "@/components/camera-mark";
import { ScoreDots } from "@/components/score-dots";
import type { PkuScore } from "@/lib/types";

const TILE = "h-24 w-24";

interface Photo {
  id: string;
  src: string;
  addedAt: number;
}

interface PhotoContextValue {
  photos: Photo[];
  addFiles: (files: FileList | null) => void;
}

const PhotoContext = createContext<PhotoContextValue | null>(null);

function storageKey(slug: string): string {
  return `phebe-photos:${slug}`;
}

function loadPhotos(slug: string): Photo[] {
  try {
    const raw = localStorage.getItem(storageKey(slug));
    if (!raw) return [];
    const parsed = JSON.parse(raw) as Photo[];
    return parsed.sort((a, b) => b.addedAt - a.addedAt);
  } catch {
    return [];
  }
}

function savePhotos(slug: string, photos: Photo[]): void {
  localStorage.setItem(storageKey(slug), JSON.stringify(photos.slice(0, 24)));
}

function readImage(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error("read"));
    reader.onload = () => {
      const src = String(reader.result ?? "");
      const img = new Image();
      img.onload = () => {
        const max = 960;
        const scale = Math.min(1, max / Math.max(img.width, img.height));
        const canvas = document.createElement("canvas");
        canvas.width = Math.round(img.width * scale);
        canvas.height = Math.round(img.height * scale);
        const ctx = canvas.getContext("2d");
        if (!ctx) {
          resolve(src);
          return;
        }
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        resolve(canvas.toDataURL("image/jpeg", 0.82));
      };
      img.onerror = () => resolve(src);
      img.src = src;
    };
    reader.readAsDataURL(file);
  });
}

function seedPhotos(urls: string[]): Photo[] {
  return urls.map((src, i) => ({
    id: `seed-${src}`,
    src,
    addedAt: urls.length - i,
  }));
}

export function PhotoProvider({
  slug,
  seed = [],
  children,
}: {
  slug: string;
  seed?: string[];
  children: React.ReactNode;
}) {
  const filed = useMemo(() => seedPhotos(seed), [seed]);
  const [uploads, setUploads] = useState<Photo[]>([]);

  useEffect(() => {
    setUploads(loadPhotos(slug));
  }, [slug]);

  const photos = useMemo(
    () => [...uploads, ...filed].sort((a, b) => b.addedAt - a.addedAt),
    [uploads, filed],
  );

  const value = useMemo<PhotoContextValue>(
    () => ({
      photos,
      addFiles(files) {
        if (!files?.length) return;
        const incoming = Array.from(files).filter((f) =>
          f.type.startsWith("image/"),
        );
        if (!incoming.length) return;
        Promise.all(incoming.map(readImage)).then((srcs) => {
          const now = Date.now();
          const added = srcs.map((src, i) => ({
            id: `${now}-${i}`,
            src,
            addedAt: now + (srcs.length - i),
          }));
          setUploads((prev) => {
            const next = [...added, ...prev].sort((a, b) => b.addedAt - a.addedAt);
            savePhotos(slug, next);
            return next;
          });
        });
      },
    }),
    [photos, slug],
  );

  return <PhotoContext.Provider value={value}>{children}</PhotoContext.Provider>;
}

function usePhotos(): PhotoContextValue {
  const ctx = useContext(PhotoContext);
  if (!ctx) {
    throw new Error("PhotoProvider");
  }
  return ctx;
}

export function LiveScoreDots({ score }: { score: PkuScore }) {
  const { photos } = usePhotos();
  return (
    <ScoreDots
      score={{
        ...score,
        phebeVerified: score.phebeVerified || photos.length > 0,
      }}
    />
  );
}

export function RestaurantPhotos() {
  const { photos, addFiles } = usePhotos();
  const inputId = useId();

  return (
    <div className="mt-6">
      <input
        id={inputId}
        type="file"
        accept="image/*"
        multiple
        className="sr-only"
        onChange={(e) => {
          addFiles(e.target.files);
          e.target.value = "";
        }}
      />
      <ul className="flex gap-2 overflow-x-auto pb-1">
        <li className={`shrink-0 ${TILE}`}>
          <label
            htmlFor={inputId}
            className={`flex ${TILE} cursor-pointer items-center justify-center rounded-lg border border-dashed border-purple/40 bg-green-pale text-purple`}
          >
            <CameraMark size={28} />
            <span className="sr-only">Add images</span>
          </label>
        </li>
        {photos.map((photo) => (
          <li key={photo.id} className={`shrink-0 ${TILE}`}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={photo.src}
              alt=""
              className={`${TILE} rounded-lg object-cover`}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}
