__int64 __fastcall sub_140ED1AC0(__int64 a1, __int64 a2, unsigned __int8 *a3)
{
  unsigned __int64 v6; // rdi
  unsigned __int64 v7; // rcx
  __int64 v8; // rdx
  __int64 v9; // r15
  __int64 **v10; // rbp
  char v11; // al
  int v12; // edx
  __int64 v13; // rax
  float v14; // xmm0_4
  unsigned __int64 v15; // rsi
  float v16; // xmm2_4
  __int64 v17; // rcx
  unsigned __int64 v18; // rdx
  unsigned __int64 v19; // rax
  __int64 v20; // rcx
  unsigned __int64 v21; // rdi
  unsigned int v22; // edi
  __int64 v23; // rbx
  unsigned __int64 v24; // rbp
  unsigned __int64 v25; // r14
  unsigned __int64 *v26; // rax
  unsigned __int64 v27; // rcx
  __int64 v28; // rax
  unsigned __int64 *v29; // rsi
  unsigned __int64 v30; // r10
  __int64 v31; // r10
  __int64 v32; // r8
  __m128i v33; // xmm0
  __int64 v34; // rdx
  __int64 v35; // rbp
  __int64 v36; // rcx
  unsigned __int64 v37; // rdx
  __int64 v38; // rax
  unsigned __int64 v39; // rcx
  unsigned __int64 *v40; // rax
  unsigned __int64 v41; // r9
  __int64 v42; // r9
  __int64 v43; // r8
  __m128i v44; // xmm0
  __int64 v45; // rdx
  unsigned __int64 v46; // rbp
  __int64 v47; // rdx
  __int64 v48; // rbp
  unsigned __int64 v49; // rsi
  __int64 v50; // rbp
  __int64 v51; // rbx
  __int64 v52; // rax
  __int64 *v53; // rcx
  __int64 *v54; // rax
  unsigned __int64 v55; // rbp
  __int64 v56; // rdx
  __int64 v57; // r8
  __int64 v58; // rdi
  __int64 *v59; // rsi
  __int64 *v60; // rbx
  int v61; // ebp
  __int64 v62; // rbp
  __int64 **v63; // r8
  _QWORD *v64; // rsi
  __int64 **v65; // rbx
  __int64 v66; // rdx
  __int64 **v67; // rbp
  _QWORD *v68; // rbx
  __int64 **v69; // rdi
  __int64 **v70; // rbp
  __int64 **v71; // rbx
  __int64 **v72; // rdi
  unsigned __int64 v73; // rax
  __int64 v74; // rdx
  __int64 v75; // rcx
  __int64 *v76; // rcx
  __int64 *v77; // rdx
  __int64 **v78; // rbx
  int v80; // [rsp+24h] [rbp-54h]
  unsigned __int64 v81; // [rsp+28h] [rbp-50h]
  __int64 v82; // [rsp+30h] [rbp-48h]

  v6 = 0x100000001B3LL
     * ((0x100000001B3LL * ((0x100000001B3LL * ((0x100000001B3LL * (*a3 ^ 0xCBF29CE484222325uLL)) ^ a3[1])) ^ a3[2]))
      ^ a3[3]);
  v7 = v6 & *(_QWORD *)(a1 + 48);
  v8 = *(_QWORD *)(a1 + 24);
  v9 = *(_QWORD *)(v8 + 16 * v7 + 8);
  if ( v9 == *(_QWORD *)(a1 + 8) )
  {
    v10 = *(__int64 ***)(v8 + 16 * v7 + 8);
  }
  else
  {
    if ( *(_DWORD *)a3 == *(_DWORD *)(v9 + 16) )
    {
LABEL_6:
      v11 = 0;
      goto LABEL_86;
    }
    v10 = *(__int64 ***)(v8 + 16 * v7);
    while ( (__int64 **)v9 != v10 )
    {
      v9 = *(_QWORD *)(v9 + 8);
      if ( *(_DWORD *)a3 == *(_DWORD *)(v9 + 16) )
        goto LABEL_6;
    }
  }
  if ( *(_QWORD *)(a1 + 16) == 0xAAAAAAAAAAAAAAALL )
  {
    sub_141758420(0x1419062C0LL);
    goto LABEL_88;
  }
  v9 = sub_141750CC0(24);
  v12 = *(_DWORD *)a3;
  *(_DWORD *)(v9 + 16) = *(_DWORD *)a3;
  v13 = *(_QWORD *)(a1 + 16) + 1LL;
  if ( v13 < 0 )
    v14 = (float)(int)(((unsigned __int64)v13 >> 1) | v13 & 1) + (float)(int)(((unsigned __int64)v13 >> 1) | v13 & 1);
  else
    v14 = (float)(int)v13;
  v15 = *(_QWORD *)(a1 + 56);
  if ( (v15 & 0x8000000000000000uLL) != 0LL )
  {
    v17 = (*(_QWORD *)(a1 + 56) >> 1) | *(_QWORD *)(a1 + 56) & 1LL;
    v16 = (float)(int)v17 + (float)(int)v17;
  }
  else
  {
    v16 = (float)(int)v15;
  }
  if ( (float)(v14 / v16) > *(float *)a1 )
  {
    v80 = v12;
    v18 = (unsigned int)(int)sub_141758C70();
    v19 = 8;
    if ( v18 >= 9 )
      v19 = v18;
    if ( v15 < v19 )
    {
      v20 = 8 * v15;
      if ( 8 * v15 < v19 )
        v20 = v19;
      if ( v15 >= 0x200 )
        v20 = v19;
      v15 = v20;
    }
    v81 = v6;
    v82 = a2;
    if ( v15 < 0x800000000000001LL )
    {
      _BitScanReverse64(&v21, (v15 - 1) | 1);
      v22 = (v21 ^ 0xFFFFFFC0) + 65;
      v23 = 1LL << v22;
      v24 = 2LL << v22;
      v25 = *(_QWORD *)(a1 + 8);
      v26 = *(unsigned __int64 **)(a1 + 24);
      v27 = *(_QWORD *)(a1 + 32);
      if ( (__int64)(v27 - (_QWORD)v26) >> 3 >= (unsigned __int64)(2LL << v22) )
      {
        if ( v26 != (unsigned __int64 *)v27 )
        {
          v30 = *(_QWORD *)(a1 + 32) - (_QWORD)v26 - 8LL;
          if ( v30 >= 0x18 )
          {
            v31 = (v30 >> 3) + 1;
            v32 = v31 & 0x3FFFFFFFFFFFFFFCLL;
            v33 = _mm_shuffle_epi32((__m128i)v25, 68);
            if ( (v31 & 0x3FFFFFFFFFFFFFFCuLL) - 4 >= 0xC )
            {
              v34 = 1LL << v22;
              v49 = ((((v31 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 0x7FFFFFFFFFFFFFFCLL;
              v35 = 0;
              do
              {
                *(__m128i *)&v26[v35] = v33;
                *(__m128i *)&v26[v35 + 2] = v33;
                *(__m128i *)&v26[v35 + 4] = v33;
                *(__m128i *)&v26[v35 + 6] = v33;
                *(__m128i *)&v26[v35 + 8] = v33;
                *(__m128i *)&v26[v35 + 10] = v33;
                *(__m128i *)&v26[v35 + 12] = v33;
                *(__m128i *)&v26[v35 + 14] = v33;
                v35 += 16;
                v49 -= 4LL;
              }
              while ( v49 != 0 );
            }
            else
            {
              v34 = 1LL << v22;
              v35 = 0;
            }
            if ( (((unsigned __int8)(((v31 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != 0 )
            {
              v50 = (__int64)&v26[v35 + 2];
              v51 = 0;
              do
              {
                *(__m128i *)(v50 + v51 - 16) = v33;
                *(__m128i *)(v50 + v51) = v33;
                v51 += 32;
              }
              while ( 32LL * (((unsigned __int8)(((v31 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != v51 );
            }
            v23 = v34;
            if ( v31 == v32 )
              goto LABEL_60;
            v26 += v32;
          }
          do
            *v26++ = v25;
          while ( v26 != (unsigned __int64 *)v27 );
        }
        goto LABEL_60;
      }
      if ( v24 <= 0x1FFFFFFFFFFFFFFFLL )
      {
        v27 = v22;
        if ( v24 < 0x200 )
        {
          v29 = (unsigned __int64 *)sub_141750CC0(16LL << v22);
          goto LABEL_35;
        }
        if ( v24 < 0x1FFFFFFFFFFFFFFCLL )
        {
          v28 = sub_141750CC0((16LL << v22) + 39);
          v29 = (unsigned __int64 *)((v28 + 39) & 0xFFFFFFFFFFFFFFE0uLL);
          *(v29 - 1) = v28;
LABEL_35:
          v36 = *(_QWORD *)(a1 + 24);
          v37 = *(_QWORD *)(a1 + 40) - v36;
          if ( v37 != 0 )
          {
            if ( v37 >= 0x1000 )
            {
              v38 = *(_QWORD *)(v36 - 8);
              v39 = v36 - 8 - v38;
              if ( v39 >= 0x20 )
                MEMORY[0x1419488E8](v39);
              v36 = v38;
            }
            sub_141750D04(v36);
          }
          *(_QWORD *)(a1 + 24) = v29;
          v40 = &v29[v24];
          *(_QWORD *)(a1 + 32) = v40;
          *(_QWORD *)(a1 + 40) = v40;
          v41 = (16LL << v22) - 8;
          if ( v41 >= 0x18 )
          {
            v42 = (v41 >> 3) + 1;
            v43 = v42 & 0x3FFFFFFFFFFFFFFCLL;
            v44 = _mm_shuffle_epi32((__m128i)v25, 68);
            if ( (v42 & 0x3FFFFFFFFFFFFFFCuLL) - 4 >= 0xC )
            {
              v46 = ((((v42 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 0x7FFFFFFFFFFFFFFCLL;
              v45 = 0;
              do
              {
                *(__m128i *)&v29[v45] = v44;
                *(__m128i *)&v29[v45 + 2] = v44;
                *(__m128i *)&v29[v45 + 4] = v44;
                *(__m128i *)&v29[v45 + 6] = v44;
                *(__m128i *)&v29[v45 + 8] = v44;
                *(__m128i *)&v29[v45 + 10] = v44;
                *(__m128i *)&v29[v45 + 12] = v44;
                *(__m128i *)&v29[v45 + 14] = v44;
                v45 += 16;
                v46 -= 4LL;
              }
              while ( v46 != 0 );
            }
            else
            {
              v45 = 0;
            }
            if ( (((unsigned __int8)(((v42 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != 0 )
            {
              v47 = (__int64)&v29[v45 + 2];
              v48 = 0;
              do
              {
                *(__m128i *)(v47 + v48 - 16) = v44;
                *(__m128i *)(v47 + v48) = v44;
                v48 += 32;
              }
              while ( 32LL * (((unsigned __int8)(((v42 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != v48 );
            }
            if ( v42 == v43 )
              goto LABEL_60;
            v29 += v43;
          }
          do
            *v29++ = v25;
          while ( v29 != v40 );
LABEL_60:
          v52 = v23 - 1;
          *(_QWORD *)(a1 + 48) = v23 - 1;
          *(_QWORD *)(a1 + 56) = v23;
          v10 = *(__int64 ***)(a1 + 8);
          v53 = *v10;
          if ( *v10 != (__int64 *)v25 )
          {
            while ( 1 )
            {
              v54 = v53;
              v55 = *(_QWORD *)(a1 + 48)
                  & (0x100000001B3LL
                   * ((0x100000001B3LL
                     * ((0x100000001B3LL
                       * ((0x100000001B3LL * (*((unsigned __int8 *)v53 + 16) ^ 0xCBF29CE484222325uLL))
                        ^ *((unsigned __int8 *)v53 + 17)))
                      ^ *((unsigned __int8 *)v53 + 18)))
                    ^ *((unsigned __int8 *)v53 + 19)));
              v53 = (__int64 *)*v53;
              v56 = *(_QWORD *)(a1 + 24);
              v57 = 2 * v55;
              v58 = 2 * v55 + 1;
              v59 = *(__int64 **)(v56 + 16 * v55);
              if ( v59 == (__int64 *)v25 )
              {
                *(_QWORD *)(v56 + 16 * v55) = v54;
              }
              else
              {
                v60 = *(__int64 **)(v56 + 8 * v58);
                v61 = *((_DWORD *)v54 + 4);
                if ( v61 != *((_DWORD *)v60 + 4) )
                {
                  while ( v59 != v60 )
                  {
                    v60 = (__int64 *)v60[1];
                    if ( v61 == *((_DWORD *)v60 + 4) )
                    {
                      v66 = *v60;
                      v67 = (__int64 **)v54[1];
                      *v67 = v53;
                      v68 = (_QWORD *)v53[1];
                      *v68 = v66;
                      v69 = *(__int64 ***)(v66 + 8);
                      *v69 = v54;
                      *(_QWORD *)(v66 + 8) = v68;
                      v53[1] = (__int64)v67;
                      v54[1] = (__int64)v69;
                      goto LABEL_64;
                    }
                  }
                  v70 = (__int64 **)v54[1];
                  *v70 = v53;
                  v71 = (__int64 **)v53[1];
                  *v71 = v59;
                  v72 = (__int64 **)v59[1];
                  *v72 = v54;
                  v59[1] = (__int64)v71;
                  v53[1] = (__int64)v70;
                  v54[1] = (__int64)v72;
                  *(_QWORD *)(v56 + 8 * v57) = v54;
                  goto LABEL_64;
                }
                v62 = *v60;
                if ( (__int64 *)*v60 != v54 )
                {
                  v63 = (__int64 **)v54[1];
                  *v63 = v53;
                  v64 = (_QWORD *)v53[1];
                  *v64 = v62;
                  v65 = *(__int64 ***)(v62 + 8);
                  *v65 = v54;
                  *(_QWORD *)(v62 + 8) = v64;
                  v53[1] = (__int64)v63;
                  v54[1] = (__int64)v65;
                }
              }
              *(_QWORD *)(v56 + 8 * v58) = v54;
LABEL_64:
              if ( v53 == (__int64 *)v25 )
              {
                v10 = *(__int64 ***)(a1 + 8);
                v52 = *(_QWORD *)(a1 + 48);
                break;
              }
            }
          }
          v6 = v81;
          v73 = v81 & v52;
          v74 = *(_QWORD *)(a1 + 24);
          v75 = *(_QWORD *)(v74 + 16 * v73 + 8);
          a2 = v82;
          if ( (__int64 **)v75 != v10 )
          {
            if ( v80 == *(_DWORD *)(v75 + 16) )
            {
LABEL_79:
              v10 = *(__int64 ***)v75;
            }
            else
            {
              v10 = *(__int64 ***)(v74 + 16 * v73);
              while ( (__int64 **)v75 != v10 )
              {
                v75 = *(_QWORD *)(v75 + 8);
                if ( v80 == *(_DWORD *)(v75 + 16) )
                  goto LABEL_79;
              }
            }
          }
          goto LABEL_80;
        }
      }
LABEL_89:
      sub_1400DAC30(v27);
    }
LABEL_88:
    sub_141758420(0x1418DE1D0LL);
    goto LABEL_89;
  }
LABEL_80:
  v76 = v10[1];
  ++*(_QWORD *)(a1 + 16);
  *(_QWORD *)v9 = v10;
  *(_QWORD *)(v9 + 8) = v76;
  *v76 = v9;
  v10[1] = (__int64 *)v9;
  v77 = (__int64 *)(*(_QWORD *)(a1 + 24) + 16 * (*(_QWORD *)(a1 + 48) & v6));
  v78 = (__int64 **)(v77 + 1);
  if ( *v77 == *(_QWORD *)(a1 + 8) )
  {
    *v77++ = v9;
LABEL_85:
    *v77 = v9;
    v11 = 1;
    goto LABEL_86;
  }
  if ( (__int64 **)*v77 == v10 )
    goto LABEL_85;
  v11 = 1;
  ++v77;
  if ( *v78 == v76 )
    goto LABEL_85;
LABEL_86:
  *(_QWORD *)a2 = v9;
  *(_BYTE *)(a2 + 8) = v11;
  return a2;
}
