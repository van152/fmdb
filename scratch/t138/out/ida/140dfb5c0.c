__int64 __fastcall sub_140DFB5C0(__int64 a1, __int64 *a2, char a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 *v8; // rsi
  char v12; // bl
  __int64 v13; // rax
  int v14; // ecx
  __int64 v15; // r8
  __int64 v16; // r8
  int v17; // edi
  __int64 v18; // r8
  int v19; // esi
  __int64 v20; // rcx
  __int64 *v21; // r12
  __int64 v22; // r8
  bool v23; // zf
  __int64 *v24; // rsi
  __int64 v25; // rbx
  _DWORD *v26; // rcx
  void (__fastcall ***v27)(_QWORD, __int64); // rcx
  bool v29; // bl
  __int64 *v30; // rsi
  __int64 v31; // rdx
  __int64 v32; // r8
  __int64 v33; // rsi
  __int64 v34; // rsi
  _QWORD *v35; // [rsp+48h] [rbp-38h] BYREF
  __int64 v36; // [rsp+50h] [rbp-30h]
  char *v37; // [rsp+58h] [rbp-28h]
  __int64 v38; // [rsp+60h] [rbp-20h] BYREF
  int v39; // [rsp+68h] [rbp-18h] BYREF
  _DWORD *v40; // [rsp+70h] [rbp-10h] BYREF
  __int64 *v41; // [rsp+78h] [rbp-8h]
  __int64 v42; // [rsp+80h] [rbp+0h]
  char *v43; // [rsp+88h] [rbp+8h]
  __int64 v44; // [rsp+90h] [rbp+10h]

  v44 = -2;
  v12 = a7;
  v13 = *a2;
  v40 = (_DWORD *)v13;
  if ( v13 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v13 + 8));
  v14 = a1 - 120;
  v43 = nullptr;
  v42 = 0;
  v41 = nullptr;
  if ( a7 == 0 )
  {
    *(_QWORD *)(a1 - 32) = 0;
    if ( a3 == 0 )
    {
LABEL_17:
      v43 = nullptr;
      v42 = 0;
      v41 = nullptr;
      LOBYTE(v8) = v40[4] == 0;
      goto LABEL_47;
    }
    v17 = *(_DWORD *)(*(_QWORD *)(a1 - 112) + 4LL) + v14 + 8;
    goto LABEL_12;
  }
  v36 = a1 - 120;
  v35 = &v40;
  sub_140DFBC70(a1: &v35, a2: a1 - 72, a3: 0);
  LOBYTE(v15) = 1;
  sub_140DFBC70(a1: &v35, a2: a1 - 64, a3: v15);
  LOBYTE(v16) = 2;
  sub_140DFBC70(a1: &v35, a2: a1 - 56, a3: v16);
  if ( (unsigned __int8)sub_140087070() != 0 )
  {
    if ( v42 != 0 && v40 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41);
    v43 = nullptr;
    v42 = 0;
    v41 = nullptr;
    sub_140814B10(a1: v40, a2: &v38, a3: a1 - 88);
    if ( (_DWORD)v38 != 0 )
      goto LABEL_46;
  }
  else
  {
    v38 = 0;
    if ( v42 != 0 && v40 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41);
    v43 = nullptr;
    v42 = 0;
    v41 = nullptr;
    sub_140814B10(a1: v40, a2: &v39, a3: &v38);
    v19 = v39;
    v20 = v38;
    if ( v38 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 - 4)) == 0 )
      sub_1412EC9A0(a1: v20 - 4);
    if ( v19 != 0 )
      goto LABEL_46;
  }
  if ( v43 == (char *)(a1 - 92) )
  {
    v21 = (__int64 *)(a1 - 16);
    v23 = v42 == -4;
    v22 = v42 + 4;
    v42 += 4;
    v43 = (char *)(a1 - 88);
    if ( v23 )
      goto LABEL_33;
  }
  else
  {
    if ( v42 != 0 && v40 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41, a3: v42);
    v41 = (__int64 *)(a1 - 92);
    v42 = 4;
    v43 = (char *)(a1 - 88);
    v21 = (__int64 *)(a1 - 16);
    v22 = 4;
  }
  if ( v40 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41, a3: v22);
LABEL_33:
  v37 = (char *)(a1 - 92);
  v41 = v21;
  v42 = 5;
  v43 = (char *)(a1 - 11);
  v24 = (__int64 *)(a1 - 48);
  if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
  {
    if ( v40 != nullptr )
    {
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v21, a3: 5);
      v41 = (__int64 *)(a1 - 48);
      v42 = 4;
      v43 = (char *)(a1 - 44);
      v25 = 8;
      if ( v40 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: a1 - 48, a3: 4);
      v24 = (__int64 *)(a1 - 40);
    }
    else
    {
      v24 = (__int64 *)(a1 - 40);
      v25 = 8;
    }
  }
  else
  {
    v25 = 16;
    if ( v40 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v21, a3: 5);
  }
  v41 = v24;
  v42 = v25;
  v43 = (char *)(a1 - 32);
  if ( v40 != nullptr )
  {
    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v24, a3: v25);
    v26 = v40;
  }
  else
  {
    v26 = nullptr;
  }
  v43 = nullptr;
  v42 = 0;
  v41 = nullptr;
  if ( v26[4] != 0 )
    goto LABEL_46;
  v41 = (__int64 *)(a1 - 24);
  v29 = HIBYTE(qword_141B6034C) != 0 && byte_141B5FC2C == 0;
  v42 = 4LL * v29 + 4;
  v43 = (char *)(a1 + 4LL * v29 - 20);
  v30 = &v38;
  if ( v43 == (char *)&v38 )
  {
    v32 = (4LL * v29 + 4) | 1;
    v42 = v32;
    v43 = (char *)&v38 + 1;
    v30 = (__int64 *)(a1 - 24);
    goto LABEL_58;
  }
  (*(void (__fastcall **)(_DWORD *))(*(_QWORD *)v26 + 40LL))(a1: v26);
  v26 = v40;
  v41 = &v38;
  v42 = 1;
  v43 = (char *)&v38 + 1;
  v32 = 1;
  if ( v40 != nullptr )
LABEL_58:
    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v26 + 40LL))(a1: v26, a2: v30, a3: v32);
  v43 = nullptr;
  v42 = 0;
  v41 = nullptr;
  if ( (_BYTE)v38 == 0 )
  {
    *(_QWORD *)(a1 - 32) = 0;
    LOBYTE(v39) = 1;
LABEL_68:
    if ( v42 != 0 && v40 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41);
    v41 = (__int64 *)&v39;
    v42 = 1;
    v43 = (char *)&v39 + 1;
    goto LABEL_72;
  }
  v33 = sub_140DFBF40(a1, a2: v31, a3: v32);
  if ( v42 != 0 && v40 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41);
  v43 = nullptr;
  v42 = 0;
  v41 = nullptr;
  if ( (unsigned __int8)sub_141400230(a1: v33, a2: &v40) == 0 )
    goto LABEL_46;
  LOBYTE(v39) = 1;
  if ( v43 != (char *)&v39 )
    goto LABEL_68;
  v23 = v42++ == -1;
  v43 = (char *)&v39 + 1;
  if ( !v23 )
  {
LABEL_72:
    if ( v40 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41);
  }
  v43 = nullptr;
  v42 = 0;
  v41 = nullptr;
  if ( (_BYTE)v39 == 0 )
  {
    v8 = (__int64 *)(a1 - 96);
    goto LABEL_84;
  }
  v34 = sub_140DFC010(a1: 24);
  sub_141457510(a1: v34);
  *(_QWORD *)(a1 - 104) = v34;
  if ( v42 != 0 && v40 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41);
  v43 = nullptr;
  v42 = 0;
  v41 = nullptr;
  if ( (unsigned __int8)sub_141457830(a1: v34, a2: &v40) != 0 )
  {
    v8 = (__int64 *)(a1 - 96);
    if ( v43 == (char *)(a1 - 96) )
    {
      v18 = v42 + 4;
      goto LABEL_85;
    }
    if ( v42 != 0 && v40 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41, a3: v42);
LABEL_84:
    v41 = v8;
    v18 = 4;
LABEL_85:
    v42 = v18;
    v43 = v37;
    if ( a3 == 0 )
    {
LABEL_14:
      if ( v18 != 0 && v40 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41);
      goto LABEL_17;
    }
    v17 = *(_DWORD *)(*(_QWORD *)(a1 - 112) + 4LL) + v36 + 8;
    if ( v18 != 0 && v40 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41);
    v12 = a7;
LABEL_12:
    v43 = nullptr;
    v42 = 0;
    v41 = nullptr;
    LODWORD(v8) = 0;
    if ( (unsigned __int8)sub_141084540(a1: v17, a2: (unsigned int)&v40, a3: 0, a4, a5, a6, a7: v12, a8) == 0 )
      goto LABEL_47;
    v18 = v42;
    goto LABEL_14;
  }
LABEL_46:
  LODWORD(v8) = 0;
LABEL_47:
  if ( v42 != 0 )
  {
    if ( v40 == nullptr )
      return (unsigned int)v8;
    (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v40 + 40LL))(a1: v40, a2: v41);
  }
  v27 = (void (__fastcall ***)(_QWORD, __int64))v40;
  v43 = nullptr;
  v42 = 0;
  v41 = nullptr;
  if ( v40 != nullptr && _InterlockedDecrement(v40 + 2) == 0 )
    (**v27)(a1: v27, a2: 1);
  return (unsigned int)v8;
}
