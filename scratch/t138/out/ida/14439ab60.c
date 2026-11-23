bool __fastcall sub_14439AB60(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  int v7; // edi
  _BYTE v9[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v9, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 4, a3: 4);
  if ( *(_DWORD *)(v5 + 16) != 0
    || (unsigned __int8)sub_140F925B0(
                          a1: (unsigned int)&qword_141B5FDA8,
                          a2: (int)a1 + 8,
                          a3: (_DWORD)a2,
                          a4: qword_141B5FDB8,
                          a5: (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
  {
    return false;
  }
  v6 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v6 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: a1, a3: 4);
  }
  v7 = *(_DWORD *)(v6 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v6 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v6)(a1: v6, a2: 1);
  return v7 == 0 && *(_DWORD *)(*a2 + 16LL) == 0;
}
