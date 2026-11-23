__int64 __fastcall sub_1415856B0(__int64 a1, _QWORD *a2, unsigned int a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v11; // rbx
  __int64 v12; // rsi
  __int64 v13; // r8
  __int64 v14; // rsi
  __int64 v15; // rsi
  __int64 v16; // rsi
  __int64 v17; // rsi
  __int64 v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 v23; // rsi
  __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 v26; // rsi
  __int64 v27; // r12
  __int64 v28; // rsi
  __int64 v29; // rsi
  __int64 v30; // rsi
  __int64 v31; // rsi
  __int64 v32; // rsi
  int v33; // edi
  __int64 v34; // rsi
  __int64 v35; // rsi
  __int64 v36; // rsi
  __int64 v37; // rsi
  __int64 v38; // rsi
  __int64 v39; // rsi
  __int64 v40; // rsi
  unsigned __int64 v41; // rax
  _BYTE *v42; // rcx
  __int64 v43; // rsi
  unsigned __int8 *v44; // rcx
  unsigned __int8 v45; // al
  __int64 v46; // rsi
  int v47; // edi
  __int64 v48; // rsi
  int v50; // [rsp+30h] [rbp-78h]
  unsigned __int8 v51; // [rsp+46h] [rbp-62h] BYREF
  char v52; // [rsp+47h] [rbp-61h] BYREF
  unsigned __int8 *v53; // [rsp+48h] [rbp-60h]
  int v54; // [rsp+50h] [rbp-58h] BYREF
  int v55; // [rsp+58h] [rbp-50h] BYREF
  __int64 v56; // [rsp+60h] [rbp-48h]

  v11 = a1 + -*(_DWORD *)(a1 - 4);
  if ( a7 != 0 )
  {
    v12 = *a2;
    if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
      v13 = 4;
    else
      v13 = 8;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 200, a3: v13);
    if ( *(_DWORD *)(v12 + 16) != 0 )
      return 0;
    v14 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 28, a3: 2);
    if ( *(_DWORD *)(v14 + 16) != 0 )
      return 0;
    v15 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 26, a3: 2);
    if ( *(_DWORD *)(v15 + 16) != 0 )
      return 0;
    v16 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 24, a3: 2);
    if ( *(_DWORD *)(v16 + 16) != 0 )
      return 0;
    v17 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 22, a3: 1);
    if ( *(_DWORD *)(v17 + 16) != 0 )
      return 0;
    v18 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 21, a3: 1);
    if ( *(_DWORD *)(v18 + 16) != 0 )
      return 0;
    v19 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 20, a3: 1);
    if ( *(_DWORD *)(v19 + 16) != 0 )
      return 0;
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 19, a3: 1);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      return 0;
    v21 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 18, a3: 1);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      return 0;
    v22 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 17, a3: 1);
    if ( *(_DWORD *)(v22 + 16) != 0 )
      return 0;
    v23 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 16, a3: 1);
    if ( *(_DWORD *)(v23 + 16) != 0 )
      return 0;
    v24 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 15, a3: 1);
    if ( *(_DWORD *)(v24 + 16) != 0 )
      return 0;
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 14, a3: 1);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      return 0;
    v51 = 0;
    v26 = *a2;
    (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v51, a3: 1);
    if ( *(_DWORD *)(v26 + 16) != 0 )
      return 0;
    if ( v51 != 0 )
    {
      v53 = (unsigned __int8 *)(v11 - 128);
      v56 = 0;
      do
      {
        if ( dword_141B65A28 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B65A28);
          if ( dword_141B65A28 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B659D8,
              a2: 1100129393,
              a3: 1024,
              a4: 32,
              a5: 0,
              a6: 0,
              a7: 1024,
              a8: 4096);
            sub_141751048(a1: sub_14158A320);
            sub_141750EA0(a1: &dword_141B65A28);
          }
        }
        v27 = sub_1407E58C0(a1: &unk_141B659D8, a2: 32);
        *(_QWORD *)(v27 + 24) = 0;
        *(_QWORD *)v27 = 0;
        *(_QWORD *)(v27 + 8) = 0;
        *(_QWORD *)(v27 + 16) = 0x76C0001FFFFFFFFLL;
        *(_DWORD *)(v27 + 27) = 0;
        *(_DWORD *)(v27 + 24) = 0;
        v28 = *a2;
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v52, a3: 1);
        if ( *(_DWORD *)(v28 + 16) != 0 )
          return 0;
        v29 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27 + 24, a3: 1);
        if ( *(_DWORD *)(v29 + 16) != 0 )
          return 0;
        v30 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27 + 25, a3: 1);
        if ( *(_DWORD *)(v30 + 16) != 0 )
          return 0;
        v31 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27 + 26, a3: 1);
        if ( *(_DWORD *)(v31 + 16) != 0 )
          return 0;
        v32 = *a2;
        if ( *a2 != 0 )
        {
          _InterlockedIncrement((volatile signed __int32 *)(v32 + 8));
          (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v32 + 40LL))(a1: v32, a2: v27 + 20, a3: 4);
        }
        v33 = *(_DWORD *)(v32 + 16);
        if ( _InterlockedDecrement((volatile signed __int32 *)(v32 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v32)(a1: v32, a2: 1);
        if ( v33 != 0 )
          return 0;
        v34 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27 + 27, a3: 1);
        if ( *(_DWORD *)(v34 + 16) != 0 )
          return 0;
        v35 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27 + 28, a3: 1);
        if ( *(_DWORD *)(v35 + 16) != 0 )
          return 0;
        v36 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27 + 16, a3: 4);
        if ( *(_DWORD *)(v36 + 16) != 0 )
          return 0;
        v37 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27 + 29, a3: 1);
        if ( *(_DWORD *)(v37 + 16) != 0 )
          return 0;
        v38 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27 + 30, a3: 1);
        if ( *(_DWORD *)(v38 + 16) != 0 )
          return 0;
        v39 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27, a3: 4);
        if ( *(_DWORD *)(v39 + 16) != 0 )
          return 0;
        v40 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27 + 8, a3: 4);
        if ( *(_DWORD *)(v40 + 16) != 0 || *(_DWORD *)(*a2 + 16LL) != 0 )
          return 0;
        v41 = *v53;
        if ( v41 > 9 )
        {
          v43 = v53[88];
          if ( *(_QWORD *)&v53[8 * v43 + 8] != 0 )
            sub_14158AC60();
          v44 = v53;
          *(_QWORD *)&v53[8 * v43 + 8] = v27;
          v45 = v44[88] + 1;
          if ( v45 >= 0xAu )
            v45 = 0;
          v44[88] = v45;
        }
        else
        {
          v42 = v53;
          *(_QWORD *)&v53[8 * v41 + 8] = v27;
          *v42 = v41 + 1;
        }
      }
      while ( ++v56 < (unsigned __int64)v51 );
    }
    sub_14096BA90(a1: &v55, a2, a3: v11 - 176);
    if ( v55 != 0 )
      return 0;
    sub_14096BA90(a1: &v54, a2, a3: v11 - 152);
    if ( v54 != 0 )
      return 0;
    v46 = *a2;
    if ( *a2 != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(v46 + 8));
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v46 + 40LL))(a1: v46, a2: v11 - 32, a3: 4);
    }
    v47 = *(_DWORD *)(v46 + 16);
    if ( _InterlockedDecrement((volatile signed __int32 *)(v46 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v46)(a1: v46, a2: 1);
    if ( v47 != 0 )
      return 0;
    v48 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 13, a3: 1);
    if ( *(_DWORD *)(v48 + 16) != 0 )
      return 0;
  }
  if ( (_BYTE)a3 == 0
    || (a3 = 0, (unsigned __int8)sub_140DFB5C0(a1: (int)v11 - 192, (_DWORD)a2, a3: 0, a4, a5, a6, a7, a8) != 0)
    && (LOBYTE(v50) = a7,
        a3 = 0,
        (unsigned __int8)sub_141084540(a1: v11, (_DWORD)a2, a3: 0, a4, a5, a6, a7: v50, a8) != 0) )
  {
    LOBYTE(a3) = 1;
  }
  return a3;
}
