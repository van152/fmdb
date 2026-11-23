__int64 __fastcall sub_14120F520(__int64 a1, int a2, __int64 a3)
{
  unsigned int v3; // esi
  volatile signed __int32 *v5; // rcx
  __int64 v6; // r8
  __int64 v7; // r13
  __int64 v8; // rbx
  __int64 v9; // rcx
  __int64 v10; // r14
  _QWORD *v11; // rcx
  __int64 *v12; // rax
  __int64 *v13; // rdi
  __int64 v14; // r8
  _QWORD *v15; // r9
  __int64 v16; // rdx
  __int64 v17; // rsi
  __int64 v18; // rbx
  __int64 *v19; // rsi
  __int64 v20; // rax
  _QWORD *v21; // rax
  __int64 i; // rdi
  _QWORD *v23; // rax
  int v24; // eax
  __int128 *v25; // r14
  char v26; // r13
  int *v27; // rax
  int *v28; // rcx
  unsigned __int64 v29; // rdx
  int v30; // ebx
  __int64 v31; // rdx
  __int64 v32; // r8
  unsigned __int64 v33; // r9
  unsigned __int64 v34; // rbx
  __m128 v35; // xmm1
  __int64 v36; // rsi
  __m128 v37; // xmm2
  __m128 v38; // xmm3
  __m128 v39; // xmm4
  __m128 v40; // xmm0
  __m128 v41; // xmm1
  __m128 v42; // xmm2
  int v43; // edx
  __int128 v44; // kr00_16
  volatile signed __int32 *v45; // rbx
  volatile signed __int32 *v46; // rbx
  volatile signed __int32 *v47; // rcx
  volatile signed __int32 *v48; // rcx
  __int64 v50; // [rsp+48h] [rbp-38h] BYREF
  __int128 v51; // [rsp+50h] [rbp-30h] BYREF
  __int64 v52; // [rsp+60h] [rbp-20h]
  volatile signed __int32 *v53; // [rsp+68h] [rbp-18h] BYREF
  __int64 **v54; // [rsp+70h] [rbp-10h]
  _QWORD *v55; // [rsp+78h] [rbp-8h]
  __int128 v56; // [rsp+80h] [rbp+0h] BYREF
  __int64 v57; // [rsp+90h] [rbp+10h]
  volatile signed __int32 *v58; // [rsp+A0h] [rbp+20h] BYREF
  int *v59; // [rsp+A8h] [rbp+28h]
  __int64 v60; // [rsp+B0h] [rbp+30h]
  __int64 *v61; // [rsp+B8h] [rbp+38h]
  int v62; // [rsp+C4h] [rbp+44h] BYREF
  __int64 v63; // [rsp+C8h] [rbp+48h] BYREF

  v63 = -2;
  v50 = 0x80100004E554C4CLL;
  sub_1407D0F70(a1: (unsigned int)&v50, a2: (unsigned int)&v53, a3: a2, a4: a1 + 24, a5: a3, a6: 0, a7: 0, 0);
  v5 = v53;
  if ( v53 == nullptr )
  {
    LOBYTE(v3) = 1;
    return v3;
  }
  _InterlockedIncrement(v53 + 2);
  v58 = v5;
  _InterlockedIncrement(v5 + 2);
  v61 = nullptr;
  v60 = 0;
  v59 = nullptr;
  if ( _InterlockedDecrement(v5 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v5)(a1: v5, a2: 1);
  sub_141210620(a1: &v51, a2: &v58, a3: a1 + 96);
  if ( (_DWORD)v51 != 0 )
  {
    v3 = 0;
    goto LABEL_79;
  }
  if ( v61 == (__int64 *)&v62 )
  {
    v6 = v60 + 4;
  }
  else
  {
    if ( v60 != 0 && v58 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v58 + 40LL))(
        a1: v58,
        a2: v59,
        a3: v60);
    v59 = &v62;
    v6 = 4;
  }
  v60 = v6;
  v61 = &v63;
  sub_1412E70A0(a1: &v58);
  v54 = (__int64 **)(a1 + 120);
  v7 = v62;
  v8 = *(_QWORD *)(a1 + 120);
  v9 = (*(_QWORD *)(a1 + 136) - v8) >> 3;
  if ( 0xAAAAAAAAAAAAAAABuLL * v9 < v62 )
  {
    if ( v62 < 0 )
      sub_1400526C0(a1: v9);
    v10 = *(_QWORD *)(a1 + 128);
    v11 = (_QWORD *)sub_1407E6360(a1: qword_141ABE200, a2: 24LL * v62);
    v12 = *(__int64 **)(a1 + 120);
    v13 = *(__int64 **)(a1 + 128);
    if ( v12 != v13 )
    {
      v14 = v8;
      v15 = v11;
      do
      {
        v16 = v12[2];
        v12[2] = 0;
        v17 = *v12;
        v18 = v12[1];
        v12[1] = 0;
        *v12 = 0;
        *v11 = v17;
        v11[1] = v18;
        v11[2] = v16;
        v12 += 3;
        v11 += 3;
      }
      while ( v12 != v13 );
      v13 = *v54;
      v8 = v14;
      v11 = v15;
    }
    if ( v13 != nullptr )
    {
      v55 = v11;
      v19 = *(__int64 **)(a1 + 128);
      if ( v13 != v19 )
      {
        do
        {
          if ( *v13 != 0 )
          {
            sub_1407E6420(a1: qword_141ABE200, a2: *v13, a3: v13[2] - *v13);
            v13[2] = 0;
            v13[1] = 0;
            *v13 = 0;
          }
          v13 += 3;
        }
        while ( v13 != v19 );
        v13 = *v54;
      }
      sub_1407E6420(a1: qword_141ABE200, a2: v13, a3: *(_QWORD *)(a1 + 136) - (_QWORD)v13);
      v11 = v55;
    }
    *(_QWORD *)(a1 + 120) = v11;
    *(_QWORD *)(a1 + 128) = (char *)v11 + v10 - v8;
    *(_QWORD *)(a1 + 136) = &v11[3 * v7];
  }
  if ( qword_141ABE200 == 0 )
  {
    if ( dword_141B59AF0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AF0);
      if ( dword_141B59AF0 == -1 )
      {
        sub_1407E5B40(a1: &unk_141B59AB0);
        sub_141751048(a1: sub_1407E6720);
        sub_141750EA0(a1: &dword_141B59AF0);
      }
    }
    qword_141ABE200 = (__int64)&unk_141B59AB0;
  }
  v51 = 0;
  v52 = 0;
  v20 = *(_QWORD *)(a1 + 144);
  if ( v20 != 0 )
    v21 = (_QWORD *)*(int *)(v20 + 24);
  else
    v21 = nullptr;
  v55 = v21;
  if ( v62 > 0 )
  {
    for ( i = 0; i < v62; ++i )
    {
      v23 = *(_QWORD **)(a1 + 144);
      if ( v23 != nullptr
        && (i >= (__int64)v55
         || (v24 = *(_DWORD *)(*v23 + (((unsigned __int64)i >> 3) & 0x1FFFFFFC)), !_bittest(&v24, i))) )
      {
        v26 = 0;
        v25 = &v51;
      }
      else
      {
        v56 = 0;
        v57 = 0;
        if ( qword_141ABE200 == 0 )
        {
          if ( dword_141B59AF0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AF0);
            if ( dword_141B59AF0 == -1 )
            {
              sub_1407E5B40(a1: &unk_141B59AB0);
              sub_141751048(a1: sub_1407E6720);
              sub_141750EA0(a1: &dword_141B59AF0);
            }
          }
          qword_141ABE200 = (__int64)&unk_141B59AB0;
        }
        v56 = 0;
        v57 = 0;
        sub_14120ED80(a1: v54, a2: &v56, a3: i);
        if ( (_QWORD)v56 != 0 )
          sub_1407E6420(a1: qword_141ABE200, a2: v56, a3: v57 - v56);
        v25 = (__int128 *)&(*v54)[3 * i];
        v26 = 1;
      }
      sub_141210620(a1: &v56, a2: &v58, a3: v25);
      if ( (_DWORD)v56 != 0 )
        goto LABEL_76;
      if ( v60 != 0 && v58 != nullptr )
        (*(void (__fastcall **)(volatile signed __int32 *, int *))(*(_QWORD *)v58 + 40LL))(a1: v58, a2: v59);
      v61 = nullptr;
      v60 = 0;
      v59 = nullptr;
      if ( WORD2(v50) < 4u )
        goto LABEL_62;
      v27 = *(int **)v25;
      v28 = *((int **)v25 + 1);
      if ( *(int **)v25 == v28 )
        goto LABEL_62;
      v29 = (char *)v28 - (char *)v27 - 4;
      v30 = 0;
      if ( v29 < 0x1C )
        goto LABEL_61;
      v31 = (v29 >> 2) + 1;
      v32 = v31 & 0x7FFFFFFFFFFFFFF8LL;
      v33 = (((v31 & 0x7FFFFFFFFFFFFFF8uLL) - 8) >> 3) + 1;
      if ( (v31 & 0x7FFFFFFFFFFFFFF8LL) == 8 )
      {
        v40 = 0;
        v36 = 0;
        if ( (v33 & 1) != 0 )
          goto LABEL_58;
      }
      else
      {
        v34 = v33 & 0xFFFFFFFFFFFFFFFEuLL;
        v35 = 0;
        v36 = 0;
        do
        {
          v37 = *(__m128 *)&v27[v36];
          v38 = *(__m128 *)&v27[v36 + 4];
          v39 = *(__m128 *)&v27[v36 + 8];
          v40 = *(__m128 *)&v27[v36 + 12];
          *(__m128i *)&v27[v36] = _mm_add_epi32(
                                    (__m128i)_mm_shuffle_ps(_mm_shuffle_ps(v35, v37, 3), v37, 152),
                                    (__m128i)v37);
          *(__m128i *)&v27[v36 + 4] = _mm_add_epi32(
                                        (__m128i)_mm_shuffle_ps(_mm_shuffle_ps(v37, v38, 3), v38, 152),
                                        (__m128i)v38);
          *(__m128i *)&v27[v36 + 8] = _mm_add_epi32(
                                        (__m128i)_mm_shuffle_ps(_mm_shuffle_ps(v38, v39, 3), v39, 152),
                                        (__m128i)v39);
          *(__m128i *)&v27[v36 + 12] = _mm_add_epi32(
                                         (__m128i)_mm_shuffle_ps(_mm_shuffle_ps(v39, v40, 3), v40, 152),
                                         (__m128i)v40);
          v36 += 16;
          v35 = v40;
          v34 -= 2LL;
        }
        while ( v34 != 0 );
        if ( (v33 & 1) != 0 )
        {
LABEL_58:
          v41 = *(__m128 *)&v27[v36];
          v42 = *(__m128 *)&v27[v36 + 4];
          *(__m128i *)&v27[v36] = _mm_add_epi32(
                                    (__m128i)_mm_shuffle_ps(_mm_shuffle_ps(v40, v41, 3), v41, 152),
                                    (__m128i)v41);
          *(__m128i *)&v27[v36 + 4] = _mm_add_epi32(
                                        (__m128i)_mm_shuffle_ps(_mm_shuffle_ps(v41, v42, 3), v42, 152),
                                        (__m128i)v42);
          v40 = v42;
        }
      }
      if ( v31 != v32 )
      {
        v27 += v32;
        v30 = _mm_cvtsi128_si32(_mm_shuffle_epi32((__m128i)v40, 255));
        do
        {
LABEL_61:
          v43 = *v27;
          *v27++ += v30;
          v30 = v43;
        }
        while ( v27 != v28 );
      }
LABEL_62:
      if ( v26 == 0 )
      {
        v44 = v51;
        sub_141210420(a1: a1 + 96, a2: *(_QWORD *)(a1 + 104), a3: v51, a4: (__int64)(*((_QWORD *)&v51 + 1) - v51) >> 2);
        if ( *((_QWORD *)&v44 + 1) != (_QWORD)v44 )
          *((_QWORD *)&v51 + 1) = v44;
      }
    }
  }
  sub_141210620(a1: &v56, a2: &v58, a3: a1 + 40);
  if ( (_DWORD)v56 != 0 )
    goto LABEL_76;
  if ( v60 != 0 && v58 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, int *))(*(_QWORD *)v58 + 40LL))(a1: v58, a2: v59);
  v61 = nullptr;
  v60 = 0;
  v59 = nullptr;
  if ( *((_DWORD *)v58 + 4) != 0 )
    goto LABEL_76;
  v3 = *(_DWORD *)(a1 + 156);
  v45 = v53;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v53 + 40LL))(
    a1: v53,
    a2: a1 + 156,
    a3: 4);
  if ( *((_DWORD *)v45 + 4) != 0 )
    goto LABEL_76;
  v46 = v53;
  (*(void (__fastcall **)(volatile signed __int32 *, __int128 *, __int64))(*(_QWORD *)v53 + 40LL))(
    a1: v53,
    a2: &v56,
    a3: 2);
  if ( *((_DWORD *)v46 + 4) != 0 )
    goto LABEL_76;
  if ( (unsigned __int16)v56 >= *(_WORD *)(a1 + 160) )
  {
    if ( v3 != *(_DWORD *)(a1 + 156) )
    {
LABEL_76:
      v3 = 0;
      goto LABEL_77;
    }
    *(_BYTE *)(a1 + 163) = 1;
  }
  else
  {
    *(_WORD *)(a1 + 160) = v56;
  }
  LOBYTE(v3) = 1;
LABEL_77:
  if ( (_QWORD)v51 != 0 )
    sub_1407E6420(a1: qword_141ABE200, a2: v51, a3: v52 - v51);
LABEL_79:
  if ( v60 == 0 )
  {
LABEL_82:
    v47 = v58;
    v61 = nullptr;
    v60 = 0;
    v59 = nullptr;
    if ( v58 != nullptr && _InterlockedDecrement(v58 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v47)(a1: v47, a2: 1);
    goto LABEL_85;
  }
  if ( v58 != nullptr )
  {
    (*(void (__fastcall **)(volatile signed __int32 *, int *))(*(_QWORD *)v58 + 40LL))(a1: v58, a2: v59);
    goto LABEL_82;
  }
LABEL_85:
  v48 = v53;
  if ( v53 != nullptr && _InterlockedDecrement(v53 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v48)(a1: v48, a2: 1);
  return v3;
}
