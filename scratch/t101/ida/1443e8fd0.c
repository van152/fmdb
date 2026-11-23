bool __fastcall sub_1443E8FD0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // r8
  __int64 v9; // rbx
  __int64 v10; // rbx
  _BYTE v12[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v12, 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140F80B80(a1, a2, (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 18, 1);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 19, 1);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 20, 1);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  LOBYTE(v8) = 4 - (byte_141B5FC2C == 0);
  if ( (unsigned __int8)sub_140F80980(a1 + 8, a2, v8) == 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 21, 1);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 16, 2);
  return *(_DWORD *)(v10 + 16) == 0 && *(_DWORD *)(*a2 + 16LL) == 0;
}
