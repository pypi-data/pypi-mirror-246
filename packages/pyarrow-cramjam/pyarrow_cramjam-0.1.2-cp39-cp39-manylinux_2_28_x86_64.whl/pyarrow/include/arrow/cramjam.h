/* Generated with cbindgen:0.26.0 */


#define CRAMJAM_MAJOR 0
#define CRAMJAM_MINOR 1
#define CRAMJAM_PATCH 1


#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#ifdef __cplusplus
namespace cramjam {
#endif // __cplusplus

#define DEFAULT_COMPRESSION_LEVEL 4

#define LZ4_ACCELERATION_MAX 65537

/**
 * All codecs supported by the de/compress and de/compress_into APIs
 */
typedef enum Codec {
  Snappy,
  SnappyRaw,
  Bzip2,
  Lz4,
  Lz4Block,
  Zstd,
  Gzip,
  Brotli,
} Codec;

/**
 * Streaming only codecs, which can create De/Compressors using the de/compressor APIs
 */
typedef enum StreamingCodec {
  StreamingBzip2,
  StreamingSnappy,
  StreamingLz4,
  StreamingZstd,
  StreamingGzip,
  StreamingBrotli,
} StreamingCodec;

typedef struct Buffer {
  const uint8_t *data;
  uintptr_t len;
  bool owned;
} Buffer;

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

/**
 * Safe to call on a nullptr
 */
void free_string(char *ptr);

void free_buffer(struct Buffer buf);

struct Buffer decompress(enum Codec codec,
                         const uint8_t *input,
                         uintptr_t input_len,
                         uintptr_t *nbytes_read,
                         uintptr_t *nbytes_written,
                         char **error);

struct Buffer compress(enum Codec codec,
                       const uint32_t *level,
                       const uint8_t *input,
                       uintptr_t input_len,
                       uintptr_t *nbytes_read,
                       uintptr_t *nbytes_written,
                       char **error);

void decompress_into(enum Codec codec,
                     const uint8_t *input,
                     uintptr_t input_len,
                     uint8_t *output,
                     uintptr_t output_len,
                     uintptr_t *nbytes_read,
                     uintptr_t *nbytes_written,
                     char **error);

void compress_into(enum Codec codec,
                   const uint32_t *level,
                   const uint8_t *input,
                   uintptr_t input_len,
                   uint8_t *output,
                   uintptr_t output_len,
                   uintptr_t *nbytes_read,
                   uintptr_t *nbytes_written,
                   char **error);

void *compressor_init(enum StreamingCodec codec, const uint32_t *level, char **error);

void free_compressor(enum StreamingCodec codec, void **compressor_ptr);

struct Buffer compressor_inner(enum StreamingCodec codec, void **compressor_ptr);

/**
 * Finish the decompression stream and return the underlying buffer, transfering ownership to caller
 */
struct Buffer compressor_finish(enum StreamingCodec codec, void **compressor_ptr, char **error);

void compressor_flush(enum StreamingCodec codec, void **compressor_ptr, char **error);

void compressor_compress(enum StreamingCodec codec,
                         void **compressor_ptr,
                         const uint8_t *input,
                         uintptr_t input_len,
                         uintptr_t *nbytes_read,
                         uintptr_t *nbytes_written,
                         char **error);

void *decompressor_init(enum StreamingCodec codec);

void free_decompressor(enum StreamingCodec codec, void **decompressor_ptr);

struct Buffer decompressor_inner(enum StreamingCodec codec, void **decompressor_ptr);

/**
 * Finish the decompression stream and return the underlying buffer, transfering ownership to caller
 */
struct Buffer decompressor_finish(enum StreamingCodec codec, void **decompressor_ptr, char **error);

void decompressor_flush(enum StreamingCodec codec, void **decompressor_ptr, char **error);

void decompressor_decompress(enum StreamingCodec codec,
                             void **decompressor_ptr,
                             const uint8_t *input,
                             uintptr_t input_len,
                             uintptr_t *nbytes_read,
                             uintptr_t *nbytes_written,
                             char **error);

uintptr_t lz4_frame_max_compression_level(void);

uintptr_t lz4_frame_max_compressed_len(uintptr_t input_len, uint32_t compression_level);

uintptr_t lz4_block_max_compressed_len(uintptr_t input_len, char **error);

uintptr_t deflate_max_compressed_len(uintptr_t input_len, int32_t level);

uintptr_t gzip_max_compressed_len(uintptr_t input_len, int32_t level);

uintptr_t zstd_max_compressed_len(uintptr_t input_len);

uintptr_t snappy_raw_max_compressed_len(uintptr_t input_len);

uintptr_t brotli_max_compressed_len(uintptr_t input_len);

intptr_t snappy_raw_decompressed_len(const uint8_t *input, uintptr_t input_len, char **error);

#ifdef __cplusplus
} // extern "C"
#endif // __cplusplus

#ifdef __cplusplus
} // namespace cramjam
#endif // __cplusplus
