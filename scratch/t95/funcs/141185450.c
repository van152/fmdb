__int64 __fastcall sub_141185450(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  __int64 v21; // rbx
  __int64 v22; // rbx
  __int64 v23; // rbx
  __int64 v24; // rbx
  __int64 v25; // rbx
  __int64 v26; // rbx
  __int64 v27; // rbx
  __int64 v28; // rbx
  __int64 v29; // rbx
  __int64 v30; // rbx
  __int64 v31; // rbx
  __int64 v32; // r8
  __int64 v33; // rcx
  __int64 v34; // rbx
  __int64 v35; // rbp
  __int64 v36; // rbx
  _DWORD *v37; // rbx
  __int64 v38; // rax
  int v39; // eax
  _DWORD *v40; // rbx
  __int64 v41; // rax
  int v42; // eax
  __int64 v43; // rbx
  __int64 v44; // rbx
  __int64 v45; // rbx
  _DWORD v46[12]; // [rsp+28h] [rbp-30h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v46[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v46, 1);
  if ( v7[4] != 0 )
    return 0;
  if ( (_BYTE)a4 != 0 )
  {
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 108, 4);
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 112, 4);
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 124, 4);
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 120, 4);
    v9 = (_DWORD *)*a2;
    v10 = *(_QWORD *)(a1 + 128);
    v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
    v46[0] = v11;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v46, 4);
    if ( v9[4] != 0 )
      return 0;
    v12 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 154, 1);
    if ( *(_DWORD *)(v12 + 16) != 0 )
      return 0;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 116, 4);
    v13 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 136, 2);
    if ( *(_DWORD *)(v13 + 16) != 0 )
      return 0;
    v14 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 138, 2);
    if ( *(_DWORD *)(v14 + 16) != 0 )
      return 0;
    v15 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 140, 2);
    if ( *(_DWORD *)(v15 + 16) != 0 )
      return 0;
    v16 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 142, 2);
    if ( *(_DWORD *)(v16 + 16) != 0 )
      return 0;
    v17 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 157, 1);
    if ( *(_DWORD *)(v17 + 16) != 0 )
      return 0;
    v18 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 159, 1);
    if ( *(_DWORD *)(v18 + 16) != 0 )
      return 0;
    v19 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 160, 1);
    if ( *(_DWORD *)(v19 + 16) != 0 )
      return 0;
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 155, 1);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      return 0;
    if ( (unsigned __int8)sub_140DB89D0(a1 + 40, a2) == 0 )
      return 0;
    if ( (unsigned __int8)sub_140DB89D0(a1 + 44, a2) == 0 )
      return 0;
    if ( (unsigned __int8)sub_140DB89D0(a1 + 48, a2) == 0 )
      return 0;
    v21 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 161, 1);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      return 0;
    v22 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 162, 1);
    if ( *(_DWORD *)(v22 + 16) != 0 )
      return 0;
    v23 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 163, 1);
    if ( *(_DWORD *)(v23 + 16) != 0 )
      return 0;
    v24 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 164, 1);
    if ( *(_DWORD *)(v24 + 16) != 0 )
      return 0;
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 165, 1);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      return 0;
    v26 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 144, 2);
    if ( *(_DWORD *)(v26 + 16) != 0 )
      return 0;
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 146, 2);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      return 0;
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 148, 2);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return 0;
    v29 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 150, 2);
    if ( *(_DWORD *)(v29 + 16) != 0 )
      return 0;
    v30 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 156, 1);
    if ( *(_DWORD *)(v30 + 16) != 0 )
      return 0;
    LOBYTE(v46[0]) = *(_QWORD *)(a1 + 24) != 0;
    v31 = *a2;
    (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v46, 1);
    if ( *(_DWORD *)(v31 + 16) != 0 )
      return 0;
    v33 = *(_QWORD *)(a1 + 24);
    if ( v33 != 0 && (unsigned __int8)sub_14159F970(v33, a2, v32) == 0 )
      return 0;
    v34 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 158, 1);
    if ( *(_DWORD *)(v34 + 16) != 0
      || (unsigned __int8)sub_140DB89D0(a1 + 32, a2) == 0
      || (unsigned __int8)sub_140DB89D0(a1 + 36, a2) == 0
      || (unsigned __int8)sub_141185290(a2, a1 + 104) == 0 )
    {
      return 0;
    }
  }
  v35 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 166, 2);
  if ( *(_DWORD *)(v35 + 16) != 0 )
    return 0;
  if ( (*(_BYTE *)(a1 + 166) & 0x10) != 0 )
  {
    sub_1408149D0(*a2, v46, a1 + 56);
    if ( v46[0] != 0 )
      return 0;
  }
  v36 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 168, 1);
  if ( *(_DWORD *)(v36 + 16) != 0 )
    return 0;
  v37 = (_DWORD *)*a2;
  v38 = *(_QWORD *)(a1 + 80);
  v39 = v38 != 0 ? *(_DWORD *)(v38 + 8) : -1;
  v46[0] = v39;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v37 + 40LL))(v37, v46, 4);
  if ( v37[4] != 0 )
    return 0;
  v40 = (_DWORD *)*a2;
  v41 = *(_QWORD *)(a1 + 88);
  v42 = v41 != 0 ? *(_DWORD *)(v41 + 8) : -1;
  v46[0] = v42;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v40 + 40LL))(v40, v46, 4);
  if ( v40[4] != 0 )
    return 0;
  v43 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 152, 2);
  if ( *(_DWORD *)(v43 + 16) != 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB89D0(a1 + 52, a2) == 0 )
    return 0;
  v44 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 96, 4);
  if ( *(_DWORD *)(v44 + 16) != 0 )
    return 0;
  v45 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 100, 4);
  if ( *(_DWORD *)(v45 + 16) != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
