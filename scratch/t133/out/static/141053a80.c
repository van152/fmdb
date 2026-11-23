bool __fastcall sub_143EE68C0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  bool result; // al
  _BYTE v9[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v9, a3: 1);
  result = *(_DWORD *)(v4 + 16) == 0
        && (v5 = *a2,
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 4),
            *(_DWORD *)(v5 + 16) == 0)
        && (v6 = *a2,
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 4, a3: 4),
            *(_DWORD *)(v6 + 16) == 0)
        && (v7 = *a2,
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 1),
            *(_DWORD *)(v7 + 16) == 0)
        && *(_DWORD *)(*a2 + 16LL) == 0;
  return result;
}
