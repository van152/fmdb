char __fastcall sub_1415D56E0(__int64 a1, int a2, _QWORD *a3)
{
  __int64 v4; // rdi
  __int64 v5; // rcx

  v4 = a1 + -*(_DWORD *)(a1 - 4);
  v5 = v4 - 240;
  if ( a2 == 1348756852 )
  {
    sub_140E24F30(a1: v5, a2: 1348756852, a3);
    sub_140DC8C00(a1: v4, a2: 1348756852, a3);
    return 1;
  }
  if ( (unsigned __int8)sub_140E24F30(a1: v5, a2, a3) != 0 )
    return 1;
  return sub_140DC8C00(a1: v4, a2, a3);
}
