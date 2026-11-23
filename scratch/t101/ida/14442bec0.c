bool __fastcall sub_14442BEC0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  int v6; // ebp
  __int64 v7; // rbx
  _DWORD *v9; // rdi
  _BYTE v10[33]; // [rsp+37h] [rbp-21h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v10, 1);
  if ( *(_DWORD *)(v4 + 16) != 0
    || (unsigned __int8)sub_140F925B0(
                          (unsigned int)&qword_141B5FDA8,
                          (int)a1 + 8,
                          (_DWORD)a2,
                          qword_141B5FDB8,
                          (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
  {
    return false;
  }
  v5 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v5 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v5 + 40LL))(v5, a1 + 16, 4);
  }
  v6 = *(_DWORD *)(v5 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v5 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v5)(v5, 1);
  if ( v6 != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 20, 1);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v9 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v9 + 40LL))(v9, a1 + 21, 1);
  return v9[4] == 0;
}
