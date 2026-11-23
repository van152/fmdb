void __fastcall sub_1412E6FF0(__int64 *a1)
{
  __int64 v2; // rcx
  _QWORD *v3; // rax
  __int64 v4; // rcx

  if ( a1[2] != 0 )
  {
    v2 = *a1;
    v3 = a1 + 1;
    if ( *a1 == 0 )
    {
      a1[3] = 0;
      a1[2] = 0;
      *v3 = 0;
      return;
    }
    (*(void (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v2 + 40LL))(a1: v2, a2: *v3);
  }
  v4 = *a1;
  a1[1] = 0;
  a1[2] = 0;
  a1[3] = 0;
  if ( v4 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v4 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v4)(a1: v4, a2: 1);
}
