from cffi import FFI
import glob

ffi = FFI()

ffi.set_source(
    "_exhaust_ma",
    """
        #include "exhaust.h"
        #include "insn.h"
        #include "sim.h"
        #include "pspace.h"
        #include "asm.h"
    """,
    sources=glob.glob("exhaust_ma/exhaust-ma/*.c"),
    include_dirs=["exhaust_ma/exhaust-ma/"],
)

ffi.cdef(
    """
    typedef unsigned char  u8_t;
    typedef unsigned short u16_t;
    typedef unsigned long  u32_t;
    typedef long           s32_t;

    typedef u16_t field_t;

    typedef struct insn_st insn_t;
    struct insn_st {
        field_t a, b;
        u16_t in;
    };

    typedef struct warrior_st warrior_t;
    struct warrior_st {
        insn_t code[ 100 ];   /* code of warrior */
        unsigned int len;        /* length of -"- */
        unsigned int start;        /* start relative to first insn */

        int have_pin;        /* does warrior have pin? */
        u32_t pin;            /* pin of warrior or garbage. */

        /* info fields -- these aren't automatically set or used */
        char *name;
        int no;                     /* warrior no. */
    };

    typedef struct pspace_st pspace_t;
    struct pspace_st {
        field_t  lastresult;    /* p-space location 0. */
        field_t *mem;        /* current p-space locations 1..PSPACESIZE-1.
                               unit offset array. */
        field_t *ownmem;        /* private locations 1..PSPACESIZE-1. */
        u32_t    len;
    };

    insn_t *sim_alloc_bufs(
        unsigned int nwar,
        unsigned int coresize,
        unsigned int processes,
        unsigned int cycles);

    insn_t *sim_alloc_bufs2(
        unsigned int nwar,
        unsigned int coresize,
        unsigned int processes,
        unsigned int cycles,
        unsigned int pspace);

    void sim_free_bufs();

    void sim_clear_core(void);

    pspace_t **sim_get_pspaces(void);
    pspace_t *sim_get_pspace(unsigned int war_id);
    void sim_clear_pspaces(void);
    void sim_reset_pspaces(void);
    int sim_load_warrior(unsigned int pos, insn_t const *code, unsigned int len);
    int sim( int nwar_arg, field_t w1_start, field_t w2_start,
     unsigned int cycles, void **ptr_result );
    int sim_mw( unsigned int nwar, const field_t *war_pos_tab,
            unsigned int *death_tab );


    int asm_line( const char *line, insn_t *in, unsigned int CORESIZE );
    void asm_file( FILE *F, warrior_t *w, unsigned int CORESIZE );
    void asm_fname( const char *fname, warrior_t *w, unsigned int CORESIZE );
    void dis1( char *s, insn_t in, unsigned int CORESIZE );
    void discore( insn_t *core, int start, int end, unsigned int CORESIZE );

    pspace_t *pspace_alloc(u32_t pspacesize);
    void pspace_free(pspace_t *p);
    field_t pspace_get(const pspace_t *p, u32_t paddr);
    void pspace_set(pspace_t *p, u32_t paddr, field_t val);
    void pspace_clear(pspace_t *p);
    void pspace_share(const pspace_t *shared, pspace_t *sharer);
    void pspace_privatise(pspace_t *p);

"""
)

if __name__ == "__main__":
    ffi.compile(verbose=True)
