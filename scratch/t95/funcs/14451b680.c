bool __fastcall sub_14451B680(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  __int64 v6; // rbx
  _DWORD *v7; // rdi
  __int64 v8; // rdx
  bool result; // al
  _BYTE v10[33]; // [rsp+27h] [rbp-21h] BYREF

  v4 = (_DWORD *)*a2;
  v10[0] = 0;
  (*(void (__fastcall **)(_DWORD *, _BYTE *, __int64))(*(_QWORD *)v4 + 40LL))(v4, v10, 1);
  result = false;
  if ( v4[4] == 0 && (unsigned __int8)sub_1415786E0(a1, a2) != 0 )
  {
    v5 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
    if ( v5[4] == 0 )
    {
      v6 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
      if ( *(_DWORD *)(v6 + 16) == 0 )
      {
        v7 = (_DWORD *)*a2;
        v8 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v7 + 40LL))(v7, v8, 4);
        if ( v7[4] == 0 )
          return true;
      }
    }
  }
  return result;
}
