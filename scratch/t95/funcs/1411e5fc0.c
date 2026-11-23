__int64 __fastcall sub_1411E5FC0(__int64 a1)
{
  __int64 *v2; // rax
  __int64 v3; // rax
  int v4; // edx
  __int64 *v5; // rax
  __int64 v6; // r8
  __int64 v7; // rax

  v2 = *(__int64 **)(a1 + 24);
  if ( (v2 == *(__int64 **)(a1 + 32) || (v3 = *v2) == 0 || *(_QWORD *)(v3 + 128) == 0)
    && (unsigned __int8)sub_1411DBBF0(a1, 2) != 0
    && ((v5 = *(__int64 **)(a1 + 24)) == *(__int64 **)(a1 + 32) ? (LODWORD(v6) = 0) : (v6 = *v5),
        LOBYTE(v4) = -86,
        (v7 = sub_1411D9CF0(a1, v4, v6, 0, 1)) != 0) )
  {
    return (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v7 + 1688LL))(v7);
  }
  else
  {
    return 0;
  }
}
