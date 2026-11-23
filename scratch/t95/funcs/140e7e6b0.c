__int64 __fastcall sub_140E7E6B0(__int64 a1)
{
  unsigned __int8 *v1; // rsi

  v1 = *(unsigned __int8 **)(a1 + 336);
  if ( v1 == nullptr )
    return 0;
  if ( (*(unsigned __int8 (__fastcall **)(_QWORD))(*(_QWORD *)v1 + 56LL))(*(_QWORD *)(a1 + 336)) == 1 )
    return v1[2229];
  if ( (*(unsigned __int8 (__fastcall **)(unsigned __int8 *))(*(_QWORD *)v1 + 1136LL))(v1) != 0 )
    return (*(__int64 (__fastcall **)(unsigned __int8 *))(*(_QWORD *)v1 + 1136LL))(v1);
  return sub_141485D40(v1);
}
