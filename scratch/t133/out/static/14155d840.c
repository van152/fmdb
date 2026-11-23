bool __fastcall sub_1444F6C80(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  bool result; // al
  _BYTE v6[7]; // [rsp+20h] [rbp-28h] BYREF
  char v7; // [rsp+27h] [rbp-21h] BYREF
  _DWORD v8[8]; // [rsp+28h] [rbp-20h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v7, a3: 1);
  result = *(_DWORD *)(v4 + 16) == 0
        && (sub_14155DA10(a1: v8, a2, a3: a1, a4: v6), v8[0] == 0)
        && *(_DWORD *)(*a2 + 16LL) == 0;
  return result;
}
