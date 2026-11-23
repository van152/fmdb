__int64 __fastcall sub_1444C39B0(__int64 a1, _QWORD *a2, int a3, int a4, int a5, int a6, int a7, __int64 a8)
{
  _DWORD *v12; // rbx
  _DWORD *v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx

  v12 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v12 + 40LL))(v12, a1 + 24, 4);
  if ( v12[4] != 0 )
    return 0;
  v13 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 28, 4);
  if ( v13[4] != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 32, 1);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 33, 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 34, 1);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  else
    return sub_140FAED40(a1, (_DWORD)a2, a3, a4, a5, a6, a7, a8);
}
