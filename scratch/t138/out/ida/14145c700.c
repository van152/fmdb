bool __fastcall sub_14145C700(__int64 *a1, _QWORD *a2)
{
  __int64 v4; // rbp
  __int64 v5; // rdx
  unsigned int *v6; // rax
  unsigned __int64 v7; // rdi
  unsigned __int64 v8; // rcx
  unsigned __int64 v9; // r13
  __int64 v10; // r12
  unsigned __int64 v11; // rax
  unsigned __int64 v12; // rcx
  unsigned __int64 v13; // r8
  unsigned __int64 v14; // r9
  __int64 v15; // rbx
  __int64 v16; // rsi
  __int64 v17; // rdi
  __m128 v18; // xmm0
  __m128 v19; // xmm1
  __m128 v20; // xmm4
  __m128 v21; // xmm5
  __m128 v22; // xmm3
  unsigned __int64 v23; // rbp
  unsigned __int64 v24; // rcx
  unsigned __int64 v25; // rdi
  unsigned __int64 v26; // rbx
  __int64 v27; // rdx
  __m128 v28; // xmm0
  __m128 v29; // xmm1
  __m128 v30; // xmm4
  __m128 v31; // xmm5
  __m128 v32; // xmm3
  __m128 v33; // xmm1
  __int64 v34; // rdx
  __int64 v35; // rdi
  unsigned __int64 v36; // rcx
  __int64 v37; // rbx
  __int64 v38; // rsi
  bool v39; // al
  _DWORD *v40; // rcx
  unsigned __int64 i; // rbp
  __int64 v42; // rdi
  bool result; // al
  __m128 v44; // xmm1
  char v45; // [rsp+2Fh] [rbp-49h] BYREF
  unsigned int v46; // [rsp+30h] [rbp-48h] BYREF
  int v47[17]; // [rsp+34h] [rbp-44h] BYREF

  if ( *a1 != a1[1] )
    a1[1] = *a1;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v46, a3: 4);
  v4 = v46;
  v5 = *a1;
  v6 = (unsigned int *)a1[1];
  v7 = ((__int64)v6 - *a1) >> 2;
  if ( v7 > v46 )
  {
    v6 = (unsigned int *)(v5 + 4LL * v46);
    goto LABEL_5;
  }
  if ( v7 < v46 )
  {
    v8 = (a1[2] - v5) >> 2;
    if ( v8 >= v46 )
    {
      v23 = v46 - v7;
      if ( v23 != 0 )
      {
        if ( v23 >= 8 )
        {
          v24 = v23 & 0xFFFFFFFFFFFFFFF8uLL;
          v25 = (((v23 & 0xFFFFFFFFFFFFFFF8uLL) - 8) >> 3) + 1;
          if ( (v23 & 0xFFFFFFFFFFFFFFF8uLL) == 8 )
          {
            v27 = 0;
          }
          else
          {
            v26 = v25 & 0xFFFFFFFFFFFFFFFEuLL;
            v27 = 0;
            v28 = (__m128)MEMORY[0x1418B7280];
            v29 = (__m128)MEMORY[0x1418B7290];
            do
            {
              v30 = *(__m128 *)&v6[v27 + 8];
              v31 = *(__m128 *)&v6[v27 + 12];
              v32 = _mm_or_ps(_mm_and_ps(*(__m128 *)&v6[v27 + 4], v28), v29);
              *(__m128 *)&v6[v27] = _mm_or_ps(_mm_and_ps(*(__m128 *)&v6[v27], v28), v29);
              *(__m128 *)&v6[v27 + 4] = v32;
              *(__m128 *)&v6[v27 + 8] = _mm_or_ps(_mm_and_ps(v30, v28), v29);
              *(__m128 *)&v6[v27 + 12] = _mm_or_ps(_mm_and_ps(v31, v28), v29);
              v27 += 16;
              v26 -= 2LL;
            }
            while ( v26 != 0 );
          }
          if ( (v25 & 1) != 0 )
          {
            v44 = _mm_or_ps(_mm_and_ps(*(__m128 *)&v6[v27 + 4], MEMORY[0x1418B7280]), MEMORY[0x1418B7290]);
            *(__m128 *)&v6[v27] = _mm_or_ps(_mm_and_ps(*(__m128 *)&v6[v27], MEMORY[0x1418B7280]), MEMORY[0x1418B7290]);
            *(__m128 *)&v6[v27 + 4] = v44;
          }
          v6 += v24;
          if ( v23 == v24 )
            goto LABEL_5;
          v23 &= 7u;
        }
        do
        {
          *v6 = *v6 & 0xFFF00000 | 0xFC000;
          ++v6;
          --v23;
        }
        while ( v23 != 0 );
      }
LABEL_5:
      a1[1] = (__int64)v6;
      goto LABEL_41;
    }
    v9 = v8 + (v8 >> 1);
    if ( v9 <= v46 )
      v9 = v46;
    if ( v8 > 0x3FFFFFFFFFFFFFFFLL - (v8 >> 1) )
      v9 = 0x3FFFFFFFFFFFFFFFLL;
    v10 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v9);
    v11 = v4 - v7;
    if ( v4 == v7 )
      goto LABEL_31;
    v12 = v10 + 4 * v7;
    if ( v11 >= 8 )
    {
      v13 = v11 & 0xFFFFFFFFFFFFFFF8uLL;
      v14 = (((v11 & 0xFFFFFFFFFFFFFFF8uLL) - 8) >> 3) + 1;
      if ( (v11 & 0xFFFFFFFFFFFFFFF8uLL) == 8 )
      {
        v17 = 0;
      }
      else
      {
        v15 = v14 & 0x3FFFFFFFFFFFFFFELL;
        v16 = v10 + 4 * v7 + 48;
        v17 = 0;
        v18 = (__m128)MEMORY[0x1418B7280];
        v19 = (__m128)MEMORY[0x1418B7290];
        do
        {
          v20 = *(__m128 *)(v16 + v17 - 16);
          v21 = *(__m128 *)(v16 + v17);
          v22 = _mm_or_ps(_mm_and_ps(*(__m128 *)(v16 + v17 - 32), v18), v19);
          *(__m128 *)(v16 + v17 - 48) = _mm_or_ps(_mm_and_ps(*(__m128 *)(v16 + v17 - 48), v18), v19);
          *(__m128 *)(v16 + v17 - 32) = v22;
          *(__m128 *)(v16 + v17 - 16) = _mm_or_ps(_mm_and_ps(v20, v18), v19);
          *(__m128 *)(v16 + v17) = _mm_or_ps(_mm_and_ps(v21, v18), v19);
          v17 += 64;
          v15 -= 2;
        }
        while ( v15 != 0 );
      }
      if ( (v14 & 1) != 0 )
      {
        v33 = _mm_or_ps(_mm_and_ps(*(__m128 *)(v12 + v17 + 16), MEMORY[0x1418B7280]), MEMORY[0x1418B7290]);
        *(__m128 *)(v12 + v17) = _mm_or_ps(_mm_and_ps(*(__m128 *)(v12 + v17), MEMORY[0x1418B7280]), MEMORY[0x1418B7290]);
        *(__m128 *)(v12 + v17 + 16) = v33;
      }
      if ( v11 == v13 )
        goto LABEL_31;
      v11 &= 7u;
      v12 += 4 * v13;
    }
    v34 = 0;
    do
    {
      *(_DWORD *)(v12 + 4 * v34) = *(_DWORD *)(v12 + 4 * v34) & 0xFFF00000 | 0xFC000;
      ++v34;
    }
    while ( v11 != v34 );
LABEL_31:
    sub_141758A00(a1: v10, a2: *a1, a3: a1[1] - *a1);
    v35 = *a1;
    if ( *a1 != 0 )
    {
      v36 = a1[2] - v35;
      if ( v36 == -1 )
        v36 = *(unsigned int *)(v35 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v37 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v37) >> 3 > v36)
        && (v38 = *(_QWORD *)(v37 + 8 * v36)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v38 + 32, a2: v35 - *(unsigned int *)(v38 + 120));
        v39 = *(_BYTE *)(v38 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 + 64)) != 0;
        if ( !v39 && *(_BYTE *)(v38 + 97) != 0 )
          sub_1412D33C0(a1: v38);
      }
      else
      {
        MEMORY[0x141948990](a1: v35 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *a1 = v10;
    a1[1] = v10 + 4 * v4;
    a1[2] = v10 + 4 * v9;
  }
LABEL_41:
  v40 = (_DWORD *)*a2;
  if ( v46 == 0 )
    return v40[4] == 0;
  for ( i = 0; i < v46; ++i )
  {
    v42 = *a1;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: &v45, a3: 1);
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v47, a3: 4);
    *(_DWORD *)(v42 + 4 * i) = ((v45 & 0x3F) << 14) | *(_DWORD *)(v42 + 4 * i) & 0xFFF00000 | v47[0] & 0x3FFF;
    v40 = (_DWORD *)*a2;
    result = *(_DWORD *)(*a2 + 16LL) == 0;
    if ( *(_DWORD *)(*a2 + 16LL) != 0 )
      break;
  }
  return result;
}
