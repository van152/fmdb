__int64 __fastcall sub_140A15F00(__int64 *a1, __int64 *a2)
{
  __int64 v4; // rsi
  int v5; // r9d
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  __int64 v7; // rcx
  __int64 v8; // rsi
  volatile signed __int32 *v9; // rsi
  __int64 v11; // rax
  unsigned __int64 v12; // r13
  __int64 *v13; // rbx
  __int64 v14; // rsi
  __int64 v15; // rsi
  __int64 v16; // rsi
  int v17; // eax
  __int64 v18; // rdi
  __int64 v19; // r14
  __int64 v20; // rsi
  __int64 v21; // rdi
  __int64 v22; // rsi
  __int64 v23; // rdi
  __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 v26; // rsi
  __int64 v27; // rsi
  __int64 v28; // rsi
  __int64 v29; // rax
  unsigned __int64 v30; // rsi
  __int64 v31; // rax
  unsigned __int64 v32; // rbx
  __int64 v33; // [rsp+28h] [rbp-28h] BYREF
  char v34[8]; // [rsp+30h] [rbp-20h] BYREF
  __int64 v35; // [rsp+38h] [rbp-18h] BYREF
  __int64 v36; // [rsp+40h] [rbp-10h] BYREF
  _QWORD v37[9]; // [rsp+48h] [rbp-8h] BYREF

  v37[1] = -2;
  sub_14080D0E0(a1: v34, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 10);
  *(_QWORD *)v4 = 0xA00000000LL;
  strcpy((char *)(v4 + 8), "comp_hosts");
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v35 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v35 = v4 + 4;
  v33 = 0x80100004E554C4CLL;
  if ( *a2 != 0
    && ((*(void (__fastcall **)(__int64, __int64 *, __int64 *, char *))(*(_QWORD *)*a2 + 224LL))(
          a1: *a2,
          a2: &v36,
          a3: &v35,
          a4: v34),
        v36 != 0) )
  {
    LOWORD(v5) = 13;
    sub_1407D1280(a1: (unsigned int)&v33, a2: (unsigned int)v37, a3: (unsigned int)&v36, a4: v5, a5: 0);
    v6 = (void (__fastcall ***)(_QWORD, __int64))v36;
    if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 + 8)) == 0 )
      (**v6)(a1: v6, a2: 1);
  }
  else
  {
    v37[0] = 0;
  }
  v7 = v35;
  if ( v35 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v35 - 4)) == 0 )
    sub_1412EC9A0(a1: v7 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  v8 = v37[0];
  if ( v37[0] == 0 )
  {
    LODWORD(a2) = 0;
    return (unsigned int)a2;
  }
  LODWORD(v36) = (unsigned __int64)(a1[1] - *a1) >> 3;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v37[0] + 40LL))(a1: v37[0], a2: &v36, a3: 4);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    goto LABEL_14;
  v11 = *a1;
  if ( a1[1] != *a1 )
  {
    v12 = 0;
    while ( 1 )
    {
      v13 = *(__int64 **)(v11 + 8 * v12);
      if ( (unsigned __int8)sub_140F80810(a1: v13[9], a2: v37, a3: (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
        goto LABEL_14;
      v14 = v37[0];
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v37[0] + 40LL))(a1: v37[0], a2: v13 + 10, a3: 2);
      if ( *(_DWORD *)(v14 + 16) != 0 )
        goto LABEL_14;
      v15 = v37[0];
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v37[0] + 40LL))(
        a1: v37[0],
        a2: (__int64)v13 + 86,
        a3: 1);
      if ( *(_DWORD *)(v15 + 16) != 0 )
        goto LABEL_14;
      v16 = v37[0];
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v37[0] + 40LL))(
        a1: v37[0],
        a2: (__int64)v13 + 87,
        a3: 1);
      if ( *(_DWORD *)(v16 + 16) != 0 )
        goto LABEL_14;
      LODWORD(v36) = (unsigned __int64)(v13[7] - v13[6]) >> 3;
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v37[0] + 40LL))(a1: v37[0], a2: &v36, a3: 4);
      v9 = (volatile signed __int32 *)v37[0];
      v17 = *(_DWORD *)(v37[0] + 16LL);
      if ( v17 == 0 )
      {
        v18 = v13[6];
        v19 = v13[7];
        if ( v18 != v19 )
        {
          while ( 1 )
          {
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v9 + 40LL))(
              a1: v9,
              a2: v18,
              a3: 2);
            if ( *((_DWORD *)v9 + 4) != 0 )
              goto LABEL_14;
            v20 = v37[0];
            v21 = v18 + 2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v37[0] + 40LL))(a1: v37[0], a2: v21, a3: 2);
            if ( *(_DWORD *)(v20 + 16) != 0 )
              goto LABEL_14;
            v22 = v37[0];
            v23 = v21 + 2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v37[0] + 40LL))(a1: v37[0], a2: v23, a3: 4);
            if ( *(_DWORD *)(v22 + 16) != 0 )
              goto LABEL_14;
            v9 = (volatile signed __int32 *)v37[0];
            if ( *(_DWORD *)(v37[0] + 16LL) != 0 )
              goto LABEL_56;
            v18 = v23 + 4;
            if ( v18 == v19 )
              goto LABEL_35;
          }
        }
      }
      if ( v17 != 0 )
        goto LABEL_14;
LABEL_35:
      (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v9 + 40LL))(
        a1: v9,
        a2: v13 + 11,
        a3: 1);
      if ( *((_DWORD *)v9 + 4) != 0 )
        goto LABEL_14;
      v24 = v37[0];
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v37[0] + 40LL))(
        a1: v37[0],
        a2: (__int64)v13 + 89,
        a3: 1);
      if ( *(_DWORD *)(v24 + 16) != 0 )
        goto LABEL_14;
      v25 = v37[0];
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v37[0] + 40LL))(
        a1: v37[0],
        a2: (__int64)v13 + 90,
        a3: 1);
      if ( *(_DWORD *)(v25 + 16) != 0 )
        goto LABEL_14;
      v26 = v37[0];
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v37[0] + 40LL))(
        a1: v37[0],
        a2: (__int64)v13 + 82,
        a3: 2);
      if ( *(_DWORD *)(v26 + 16) != 0 )
        goto LABEL_14;
      v27 = v37[0];
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v37[0] + 40LL))(
        a1: v37[0],
        a2: (__int64)v13 + 84,
        a3: 2);
      if ( *(_DWORD *)(v27 + 16) != 0 )
        goto LABEL_14;
      v28 = v37[0];
      LODWORD(v36) = (unsigned __int64)(v13[1] - *v13) >> 3;
      a2 = &v36;
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v37[0] + 40LL))(a1: v37[0], a2: &v36, a3: 4);
      if ( *(_DWORD *)(v28 + 16) != 0 )
        goto LABEL_14;
      v29 = *v13;
      if ( v13[1] != *v13 )
      {
        v30 = 0;
        while ( (unsigned __int8)sub_1409FD6F0(a1: *(_QWORD *)(v29 + 8 * v30), a2: v37) != 0 )
        {
          ++v30;
          v29 = *v13;
          if ( v30 >= (v13[1] - *v13) >> 3 )
            goto LABEL_45;
        }
        goto LABEL_14;
      }
LABEL_45:
      sub_1409FD830(a1: &v36, a2: v37, a3: v13 + 3);
      if ( (_DWORD)v36 != 0 )
        goto LABEL_14;
      v9 = (volatile signed __int32 *)v37[0];
      if ( *(_DWORD *)(v37[0] + 16LL) != 0 )
      {
LABEL_56:
        LODWORD(a2) = 0;
        if ( _InterlockedDecrement(v9 + 2) != 0 )
          return (unsigned int)a2;
        goto LABEL_17;
      }
      ++v12;
      v11 = *a1;
      if ( v12 >= (a1[1] - *a1) >> 3 )
        goto LABEL_50;
    }
  }
  v9 = (volatile signed __int32 *)v37[0];
LABEL_50:
  LODWORD(v36) = (unsigned __int64)(a1[4] - a1[3]) >> 3;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v9 + 40LL))(
    a1: v9,
    a2: &v36,
    a3: 4);
  if ( *((_DWORD *)v9 + 4) != 0 )
  {
LABEL_14:
    LODWORD(a2) = 0;
    goto LABEL_15;
  }
  v31 = a1[3];
  if ( a1[4] == v31 )
  {
    LOBYTE(a2) = 1;
  }
  else
  {
    v32 = 0;
    do
    {
      LODWORD(a2) = sub_1409FFE10(a1: *(_QWORD *)(v31 + 8 * v32), a2: v37);
      if ( (_BYTE)a2 == 0 )
        break;
      ++v32;
      v31 = a1[3];
    }
    while ( v32 < (a1[4] - v31) >> 3 );
  }
LABEL_15:
  v9 = (volatile signed __int32 *)v37[0];
  if ( v37[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v37[0] + 8LL)) == 0 )
LABEL_17:
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v9)(a1: v9, a2: 1);
  return (unsigned int)a2;
}
