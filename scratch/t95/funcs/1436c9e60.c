__int64 __fastcall sub_1436C9E60(_QWORD *a1, __int64 a2)
{
  int v4; // eax
  __int64 result; // rax

  sub_1412D5BA0(a1);
  v4 = 2 * *(unsigned __int8 *)(a2 + 13);
  *(_DWORD *)(a1[2] + 12LL) = v4 | *(_DWORD *)(a1[2] + 12LL) & 0xFFFFFFFD;
  *(_DWORD *)(a1[3] + 12LL) = v4 | *(_DWORD *)(a1[3] + 12LL) & 0xFFFFFFFD;
  *(_DWORD *)(a1[2] + 12LL) = *(_DWORD *)(a1[2] + 12LL) & 0xFFFFFFFE | (*(_BYTE *)(a2 + 12) == 0);
  *(_DWORD *)(a1[3] + 12LL) = *(_DWORD *)(a1[3] + 12LL) & 0xFFFFFFFE | (*(_BYTE *)(a2 + 12) == 0);
  (*(void (__fastcall **)(_QWORD, _QWORD, _QWORD))(*(_QWORD *)a1[3] + 40LL))(
    a1[3],
    *(_QWORD *)a2,
    *(unsigned int *)(a2 + 8));
  result = a1[1];
  *(_DWORD *)(result + 32) = 0;
  return result;
}
