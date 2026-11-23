__int64 __fastcall sub_1442A7730(__int64 a1, _DWORD **a2)
{
  _DWORD *v4; // rbx

  v4 = *a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v4 + 40LL))(a1: v4, a2: a1 + 16, a3: 2);
  if ( v4[4] != 0 )
    return 0;
  else
    return sub_1413C4780(a1, a2);
}
