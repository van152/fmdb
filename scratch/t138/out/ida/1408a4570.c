__int64 __fastcall sub_1408A4570(_QWORD *a1, __int64 a2)
{
  unsigned int v4; // eax
  __int64 v5; // rax
  __int64 v6; // rdi
  __int64 v7; // rbx
  __int64 v8; // r8
  __int64 v9; // rcx
  __int64 v10; // r8
  __int64 v11; // rax
  __int64 v12; // rcx
  unsigned __int64 v13; // r12
  __int64 v14; // rsi
  __int64 v15; // rbx
  __int64 v16; // rax
  __int64 v17; // r13
  __int64 v18; // r15
  __int64 v19; // r13
  bool v20; // zf
  __int64 v21; // rdi
  char v22; // bl
  __int64 v23; // rdx
  __int64 v24; // r8
  __int64 v25; // r15
  __int64 i; // rsi
  __int64 v27; // rcx
  void (__fastcall ***v28)(_QWORD, __int64); // rcx
  unsigned int v29; // r15d
  unsigned __int64 v30; // rcx
  __int64 v31; // rbx
  __int64 v32; // rsi
  __int64 v34; // r13
  __int64 v35; // rax
  __int64 v36; // rax
  __int64 *v37; // rdi
  __int64 *v38; // rsi
  __int64 v39; // rcx
  char v40; // bl
  void (__fastcall ***v41)(_QWORD, __int64); // rcx
  __int64 v42; // rdx
  __int64 v43; // r8
  void (__fastcall ***v44)(_QWORD, __int64); // rcx
  void (__fastcall ***v45)(_QWORD, __int64); // rcx
  int v46; // [rsp+20h] [rbp-60h]
  int v47; // [rsp+20h] [rbp-60h]
  int v48; // [rsp+20h] [rbp-60h]
  int v49; // [rsp+28h] [rbp-58h]
  int v50; // [rsp+28h] [rbp-58h]
  int v51; // [rsp+28h] [rbp-58h]
  _BYTE v52[8]; // [rsp+40h] [rbp-40h] BYREF
  __int64 v53; // [rsp+48h] [rbp-38h]
  __int64 v54; // [rsp+50h] [rbp-30h]
  __int64 v55; // [rsp+58h] [rbp-28h]
  __int128 v56; // [rsp+60h] [rbp-20h] BYREF
  __int64 v57; // [rsp+70h] [rbp-10h]
  __int64 v58; // [rsp+80h] [rbp+0h] BYREF
  _QWORD v59[9]; // [rsp+88h] [rbp+8h] BYREF

  v59[1] = -2;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v56 = 0;
  v57 = 0;
  v4 = sub_1400015B0();
  v5 = (*(__int64 (__fastcall **)(_QWORD *, _QWORD))(*a1 + 616LL))(a1, a2: v4);
  a1[1] = v5;
  if ( v5 == 0 )
  {
    v6 = qword_141B5AD60;
    v59[0] = 0;
    v7 = sub_1412EC810(a1: 264, a2: 84);
    *(_QWORD *)v7 = 0x5400000000LL;
    sub_1417589F0(a1: v7 + 8, a2: 0x1418F3094LL, a3: 84);
    *(_BYTE *)(v7 + 92) = 0;
    if ( v59[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v59[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v59[0] - 4LL);
    v59[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v7);
    v59[0] = v7 + 4;
    LOBYTE(v8) = 1;
    (*(void (__fastcall **)(__int64, _QWORD *, __int64, _QWORD))(*(_QWORD *)v6 + 120LL))(a1: v6, a2: v59, a3: v8, a4: 0);
    v9 = v59[0];
    if ( v59[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v59[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v9 - 4);
    v5 = a1[1];
  }
  v53 = a2;
  (*(void (__fastcall **)(__int64))(*(_QWORD *)v5 + 8LL))(a1: v5);
  v11 = a1[2];
  v12 = a1[3];
  v13 = (v12 - v11) >> 3;
  v54 = v11;
  v55 = v12;
  if ( v12 != v11 )
  {
    v14 = 1;
    if ( v13 >= 2 )
      v14 = (v12 - v11) >> 3;
    v15 = 0;
    do
    {
      v16 = *(_QWORD *)(a1[2] + 8 * v15);
      if ( *(_BYTE *)(v16 + 68) != 0 )
      {
        v17 = *(_QWORD *)(v16 + 632);
        v18 = *(_QWORD *)(v16 + 640);
        if ( v17 != v18 )
        {
          v19 = v17 + 8;
          do
          {
            LOBYTE(v10) = 1;
            if ( (unsigned __int8)sub_1408BC7F0(a1: *(_QWORD *)(v19 - 8), a2: &v56, a3: v10) == 0 )
              break;
            v20 = v19 == v18;
            v19 += 8;
          }
          while ( !v20 );
        }
      }
      ++v15;
    }
    while ( v15 != v14 );
  }
  sub_140A1E950(a1: a1[1], a2: &v56);
  sub_1408A2800(a1: &v56);
  v21 = v53;
  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, __int64))(*(_QWORD *)a1[1] + 976LL))(a1: a1[1], a2: v53) != 0
    && (sub_14080D0E0(a1: v52, a2: 0x1418E2C24LL),
        v59[0] = 0x80100004E554C4CLL,
        sub_1407D0F70(
          a1: (unsigned int)v59,
          a2: (unsigned int)&v58,
          a3: v21,
          a4: (unsigned int)&qword_141B5ACB8,
          a5: (__int64)v52,
          a6: 0,
          a7: 0,
          a8: 0),
        v58 != 0) )
  {
    sub_1409F9150(a1: a1[10]);
    LOBYTE(v49) = 0;
    LOBYTE(v46) = 1;
    v22 = 1;
    LOBYTE(v23) = 1;
    (*(void (__fastcall **)(_QWORD *, __int64, _QWORD, _QWORD, int, int))(*a1 + 656LL))(
      a1,
      a2: v23,
      a3: 0,
      a4: 0,
      a5: v46,
      a6: v49);
    if ( v55 == v54 )
    {
LABEL_63:
      LOBYTE(v50) = 0;
      LOBYTE(v47) = 1;
      v29 = 0;
      LOBYTE(v24) = 1;
      (*(void (__fastcall **)(_QWORD *, _QWORD, __int64, _QWORD, int, int))(*a1 + 656LL))(
        a1,
        a2: 0,
        a3: v24,
        a4: 0,
        a5: v47,
        a6: v50);
      LOBYTE(v51) = 1;
      LOBYTE(v48) = 0;
      LOBYTE(v42) = 1;
      LOBYTE(v43) = 1;
      (*(void (__fastcall **)(_QWORD *, __int64, __int64, _QWORD, int, int))(*a1 + 656LL))(
        a1,
        a2: v42,
        a3: v43,
        a4: 0,
        a5: v48,
        a6: v51);
      sub_140A1E400();
      *(_BYTE *)(a1[10] + 48LL) = 1;
      if ( (v22 & 1) != 0 )
      {
        v44 = (void (__fastcall ***)(_QWORD, __int64))v58;
        if ( v58 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v58 + 8)) == 0 )
          (**v44)(a1: v44, a2: 1);
        v58 = 0;
        sub_140B0B320(a1: *(_QWORD *)(a1[1] + 128LL));
        LOBYTE(v29) = 1;
      }
    }
    else
    {
      v25 = 1;
      if ( v13 >= 2 )
        v25 = v13;
      v22 = 1;
      for ( i = 0; i != v25; ++i )
      {
        if ( v22 != 0 )
        {
          v27 = *(_QWORD *)(a1[2] + 8 * i);
          v59[0] = v58;
          if ( v58 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v58 + 8));
          v22 = sub_14087EA20(a1: v27, a2: v59, a3: v21, a4: a1);
          v28 = (void (__fastcall ***)(_QWORD, __int64))v59[0];
          if ( v59[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v59[0] + 8LL)) == 0 )
            (**v28)(a1: v28, a2: 1);
        }
        else
        {
          v22 = 0;
        }
      }
      v34 = 0;
      while ( 1 )
      {
        v36 = *(_QWORD *)(a1[2] + 8 * v34);
        v37 = *(__int64 **)(v36 + 632);
        v38 = *(__int64 **)(v36 + 640);
        if ( v37 != v38 )
        {
          while ( (v22 & 1) != 0 )
          {
            v39 = *v37;
            v59[0] = v58;
            if ( v58 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v58 + 8));
            v40 = sub_1408C9150(a1: v39, a2: v59);
            v41 = (void (__fastcall ***)(_QWORD, __int64))v59[0];
            if ( v59[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v59[0] + 8LL)) == 0 )
              (**v41)(a1: v41, a2: 1);
            if ( v40 == 0 )
              break;
            ++v37;
            v22 = 1;
            if ( v37 == v38 )
              goto LABEL_52;
          }
          v35 = (*(__int64 (__fastcall **)(_QWORD *))(*a1 + 1432LL))(a1);
          v22 = 1;
          if ( v35 != 0 )
            break;
        }
LABEL_52:
        if ( ++v34 == v25 )
          goto LABEL_63;
      }
      (*(void (__fastcall **)(_QWORD *, __int64))(*a1 + 1440LL))(a1, a2: v35);
      v29 = 0;
    }
    v45 = (void (__fastcall ***)(_QWORD, __int64))v58;
    if ( v58 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v58 + 8)) == 0 )
      (**v45)(a1: v45, a2: 1);
  }
  else
  {
    v29 = 0;
  }
  if ( (_QWORD)v56 != 0 )
  {
    v30 = v57 - v56;
    if ( v57 - (_QWORD)v56 == -1 )
    {
      v30 = *(unsigned int *)(v56 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_48:
        MEMORY[0x141948990](a1: v56 - *(unsigned int *)(qword_141ABD470 + 48));
        return v29;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_48;
    }
    v31 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v31) >> 3 <= v30 )
      goto LABEL_48;
    v32 = *(_QWORD *)(v31 + 8 * v30);
    if ( v32 == 0 )
      goto LABEL_48;
    MEMORY[0x1419475D8](a1: v32 + 32, a2: v56 - *(unsigned int *)(v32 + 120));
    if ( (*(_BYTE *)(v32 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) == 0)
      && *(_BYTE *)(v32 + 97) != 0 )
    {
      sub_1412D33C0(a1: v32);
    }
  }
  return v29;
}
