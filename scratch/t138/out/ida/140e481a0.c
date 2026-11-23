__int64 __fastcall sub_140E481A0(_QWORD *a1, int a2, int a3, __int16 a4)
{
  __int64 result; // rax
  __int64 v6; // rdx
  __int64 v7; // rcx
  __int64 *v8; // rdi
  volatile signed __int32 *v9; // rsi
  volatile signed __int32 *v10; // rcx
  volatile signed __int32 *v11; // rbx
  __int64 v12; // rsi
  volatile signed __int32 *v13; // rcx
  __int64 v14; // rcx
  _QWORD *v15; // rsi
  __int64 v16; // r15
  char *v17; // rdi
  char v18; // r13
  char *v19; // r14
  bool v20; // zf
  char *v21; // r12
  char v22; // al
  __int64 v23; // rcx
  __int64 v24; // rbx
  __int64 v25; // rcx
  __int64 v26; // rax
  __int64 v27; // r14
  char v28; // al
  __int64 v29; // rcx
  __int64 v30; // rsi
  __int64 v31; // rcx
  unsigned int v32; // ebx
  char v33; // al
  char v34; // si
  char v35; // dl
  char v36; // cl
  __int64 v37; // rcx
  __int64 v38; // rcx
  __int64 v39; // rcx
  __int64 v40; // rcx
  __int64 v41; // rbx
  __int64 v42; // rsi
  unsigned int v43; // eax
  __int64 (__fastcall ***v44)(_QWORD, __int64); // rcx
  _QWORD *v45; // [rsp+28h] [rbp-58h]
  __int64 v46; // [rsp+30h] [rbp-50h]
  _QWORD *v47; // [rsp+38h] [rbp-48h]
  volatile signed __int32 *v48; // [rsp+40h] [rbp-40h]
  char *v49; // [rsp+48h] [rbp-38h]
  int v50; // [rsp+50h] [rbp-30h] BYREF
  int v51; // [rsp+54h] [rbp-2Ch] BYREF
  __int64 v52; // [rsp+58h] [rbp-28h] BYREF
  _BYTE v53[14]; // [rsp+60h] [rbp-20h] BYREF
  __int16 v54; // [rsp+6Eh] [rbp-12h] BYREF
  volatile signed __int32 *v55; // [rsp+70h] [rbp-10h] BYREF
  _QWORD v56[9]; // [rsp+78h] [rbp-8h] BYREF

  v56[1] = -2;
  v54 = a4;
  v50 = a3;
  v51 = a2;
  result = **(_QWORD **)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
  v6 = *(_QWORD *)(result + 8);
  v7 = result;
  if ( *(_BYTE *)(v6 + 25) == 0 )
  {
    v7 = **(_QWORD **)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    do
    {
      v8 = (__int64 *)(v6 + 16);
      if ( *(_QWORD *)(v6 + 32) >= (unsigned __int64)qword_141B5EDF0 )
      {
        v7 = v6;
        v8 = (__int64 *)v6;
      }
      v6 = *v8;
    }
    while ( *(_BYTE *)(*v8 + 25) == 0 );
  }
  if ( *(_BYTE *)(v7 + 25) != 0 )
    return result;
  if ( (unsigned __int64)qword_141B5EDF0 < *(_QWORD *)(v7 + 32) )
    return result;
  if ( v7 == result )
    return result;
  v9 = *(volatile signed __int32 **)(v7 + 40);
  if ( v9 == nullptr )
    return result;
  _InterlockedIncrement(v9 + 2);
  (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v9 + 120LL))(
    a1: v9,
    a2: &v55);
  v10 = v55;
  result = (unsigned int)_InterlockedExchangeAdd(v9 + 2, 0xFFFFFFFF);
  v11 = v9;
  if ( v9 == v10 )
  {
    if ( (_DWORD)result == 1 )
    {
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v9)(a1: v9, a2: 1);
      v11 = v9;
    }
  }
  else
  {
    if ( (_DWORD)result == 1 )
      result = (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v9)(a1: v9, a2: 1);
    v11 = v55;
    if ( v55 == nullptr )
      return result;
  }
  sub_14080D0E0(a1: v53, a2: 0x1418E2C24LL);
  v12 = sub_1412EC810(a1: 264, a2: 10);
  *(_QWORD *)v12 = 0xA00000000LL;
  *(_QWORD *)(v12 + 8) = MEMORY[0x1418D9738];
  *(_WORD *)(v12 + 16) = MEMORY[0x1418D9740];
  *(_BYTE *)(v12 + 18) = 0;
  _InterlockedIncrement((volatile signed __int32 *)v12);
  v52 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v12);
  v52 = v12 + 4;
  v48 = v11;
  result = (*(__int64 (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64 *, _BYTE *))(*(_QWORD *)v11 + 224LL))(
             a1: v11,
             a2: &v55,
             a3: &v52,
             a4: v53);
  if ( v55 != nullptr )
  {
    result = (*(__int64 (__fastcall **)(volatile signed __int32 *, _QWORD *, _QWORD))(*(_QWORD *)v55 + 176LL))(
               a1: v55,
               a2: v56,
               a3: 0);
    v13 = v55;
    if ( v55 != nullptr && _InterlockedDecrement(v55 + 2) == 0 )
      result = (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v13)(a1: v13, a2: 1);
  }
  else
  {
    v56[0] = 0;
  }
  v14 = v52;
  if ( v52 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v52 - 4)) == 0 )
    result = sub_1412EC9A0(a1: v14 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v12) == 0 )
    result = sub_1412EC9A0(a1: v12);
  if ( v56[0] == 0 )
    goto LABEL_75;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v56[0] + 40LL))(a1: v56[0], a2: 0x14187B81CLL, a3: 1);
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)v56[0] + 40LL))(a1: v56[0], a2: &v51, a3: 4);
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)v56[0] + 40LL))(a1: v56[0], a2: &v50, a3: 4);
  (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)v56[0] + 40LL))(a1: v56[0], a2: &v54, a3: 2);
  v15 = (_QWORD *)qword_141B5FE90;
  v46 = qword_141B5FE98;
  if ( qword_141B5FE90 == qword_141B5FE98 )
    goto LABEL_66;
  v47 = a1;
  while ( 2 )
  {
    v49 = (char *)a1[1];
    if ( (char *)*a1 == v49 )
      goto LABEL_31;
    v45 = v15;
    v16 = *v15;
    v17 = (char *)(*a1 + 2LL);
    v18 = 0;
    v19 = (char *)a1[1];
    do
    {
      v21 = v17 - 2;
      v53[0] = -1;
      v22 = *v17;
      if ( *v17 == 1 )
      {
        v23 = v16 + *(int *)(*(_QWORD *)(v16 + 8) + 4LL) + 8;
        if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v23 + 1720LL))(a1: v23) != 0 )
        {
          v24 = *v21;
          v25 = v16 + *(int *)(*(_QWORD *)(v16 + 8) + 4LL) + 8;
          v26 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v25 + 1720LL))(a1: v25);
          if ( v24 == -1 )
          {
            v28 = 0;
          }
          else
          {
            v27 = v26;
            sub_14085D820(a1: (unsigned int)v24);
            v28 = *(_BYTE *)(v27 + v24 + 520);
          }
          v53[0] = v28;
          v19 = v49;
        }
        v22 = *v17;
      }
      if ( v22 == 0 )
      {
        v29 = v16 + *(int *)(*(_QWORD *)(v16 + 8) + 4LL) + 8;
        if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v29 + 1688LL))(a1: v29) != 0 )
        {
          v30 = *v21;
          v31 = v16 + *(int *)(*(_QWORD *)(v16 + 8) + 4LL) + 8;
          v53[0] = *(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v31 + 1688LL))(a1: v31) + v30 + 24);
        }
      }
      v32 = (unsigned __int8)*(v17 - 1);
      v33 = 1;
      v34 = 1;
      if ( v32 >= 2 )
      {
        v34 = 1;
        if ( v32 != 3 )
        {
          if ( v32 == 2 )
          {
            v35 = v53[0];
            v36 = 0;
LABEL_55:
            v33 = 0;
            goto LABEL_56;
          }
          v34 = 0;
        }
      }
      v35 = v53[0];
      v36 = v34 & (v53[0] == 0);
      if ( v32 - 1 < 3 || *(v17 - 1) != 0 )
        goto LABEL_55;
LABEL_56:
      if ( ((v35 > 0) & (unsigned __int8)v33) != 0 || v36 != 0 )
      {
        if ( (v18 & 1) == 0 )
        {
          LODWORD(v55) = *(_DWORD *)(*(int *)(*(_QWORD *)(v16 + 8) + 4LL) + v16 + 20);
          (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, __int64))(*(_QWORD *)v56[0] + 40LL))(
            a1: v56[0],
            a2: &v55,
            a3: 4);
          v37 = v16 + *(int *)(*(_QWORD *)(v16 + 8) + 4LL) + 8;
          if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v37 + 1720LL))(a1: v37) != 0 )
          {
            v38 = v16 + *(int *)(*(_QWORD *)(v16 + 8) + 4LL) + 8;
            LOWORD(v55) = *(_WORD *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v38 + 1720LL))(a1: v38) + 512);
          }
          else
          {
            LOWORD(v55) = 0;
          }
          (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, __int64))(*(_QWORD *)v56[0] + 40LL))(
            a1: v56[0],
            a2: &v55,
            a3: 2);
          v39 = v16 + *(int *)(*(_QWORD *)(v16 + 8) + 4LL) + 8;
          if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v39 + 1688LL))(a1: v39) != 0 )
          {
            v40 = v16 + *(int *)(*(_QWORD *)(v16 + 8) + 4LL) + 8;
            LOWORD(v55) = *(_WORD *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v40 + 1688LL))(a1: v40) + 214);
          }
          else
          {
            LOWORD(v55) = 0;
          }
          (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, __int64))(*(_QWORD *)v56[0] + 40LL))(
            a1: v56[0],
            a2: &v55,
            a3: 2);
          v18 = 1;
        }
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)v56[0] + 40LL))(a1: v56[0], a2: v17, a3: 1);
        (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)v56[0] + 40LL))(a1: v56[0], a2: v53, a3: 1);
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)v56[0] + 40LL))(a1: v56[0], a2: v17 - 2, a3: 1);
      }
      v20 = v17 + 1 == v19;
      v17 += 3;
    }
    while ( !v20 );
    a1 = v47;
    v15 = v45;
    if ( (v18 & 1) != 0 )
    {
      LOBYTE(v55) = -1;
      (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, __int64))(*(_QWORD *)v56[0] + 40LL))(
        a1: v56[0],
        a2: &v55,
        a3: 1);
    }
LABEL_31:
    if ( ++v15 != (_QWORD *)v46 )
      continue;
    break;
  }
LABEL_66:
  LODWORD(v55) = -1;
  (*(void (__fastcall **)(_QWORD, volatile signed __int32 **, __int64))(*(_QWORD *)v56[0] + 40LL))(
    a1: v56[0],
    a2: &v55,
    a3: 4);
  v41 = a1[1];
  if ( *a1 != v41 )
  {
    v42 = *a1 + 2LL;
    do
    {
      v43 = *(unsigned __int8 *)(v42 - 1);
      if ( v43 <= 3 && v43 != 1 )
      {
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v56[0] + 40LL))(a1: v56[0], a2: v42, a3: 1);
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v56[0] + 40LL))(a1: v56[0], a2: v42 - 2, a3: 1);
      }
      v20 = v42 + 1 == v41;
      v42 += 3;
    }
    while ( !v20 );
  }
  LOBYTE(v55) = -1;
  result = (*(__int64 (__fastcall **)(_QWORD, volatile signed __int32 **, __int64))(*(_QWORD *)v56[0] + 40LL))(
             a1: v56[0],
             a2: &v55,
             a3: 1);
  v44 = (__int64 (__fastcall ***)(_QWORD, __int64))v56[0];
  if ( v56[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v56[0] + 8LL)) == 0 )
    result = (**v44)(a1: v44, a2: 1);
LABEL_75:
  if ( _InterlockedDecrement(v48 + 2) == 0 )
    return (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v48)(a1: v48, a2: 1);
  return result;
}
