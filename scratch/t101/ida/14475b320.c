bool __fastcall sub_14475B320(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  _DWORD *v10; // rdi
  unsigned __int8 v11; // [rsp+2Eh] [rbp-1Ah] BYREF
  _BYTE v12[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v12, 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1, 4);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 4, 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  if ( v12[0] >= 2u )
  {
    v8 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
    if ( *(_DWORD *)(v8 + 16) == 0 )
      goto LABEL_10;
    return false;
  }
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v11, 1);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  *(float *)(a1 + 8) = (float)v11;
LABEL_10:
  v10 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, a1 + 12, 1);
  return v10[4] == 0;
}
