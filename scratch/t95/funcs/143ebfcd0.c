__int64 __fastcall sub_143EBFCD0(__int64 a1, _QWORD *a2, __int64 a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v11; // rbp
  __int64 v12; // rbp
  __int64 v13; // rbp
  __int64 v14; // rbp
  __int64 v15; // rbp
  __int64 v16; // rbp
  __int64 v17; // rbp
  unsigned int v18; // ebp
  __int64 v20; // rbp
  _DWORD v21[10]; // [rsp+40h] [rbp-28h] BYREF

  sub_140814B10(*a2, v21, a1 + 24);
  if ( v21[0] != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 58, 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 59, 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 60, 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 52, 2);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 54, 2);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 56, 2);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 40, 4);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  if ( *(unsigned __int16 *)(a4 + 1416) < 0xDE7u )
  {
    *(_DWORD *)(a1 + 48) = -1;
  }
  else
  {
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 48, 4);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      return 0;
  }
  v18 = 0;
  if ( (unsigned __int8)sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8) != 0 )
  {
    if ( *(int *)(a1 + 48) <= 0 )
      *(_DWORD *)(a1 + 48) = *(_DWORD *)(a1 + 12);
    sub_141038280(a1);
    LOBYTE(v18) = 1;
  }
  return v18;
}
