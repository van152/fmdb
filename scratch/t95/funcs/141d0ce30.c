__int64 __fastcall sub_141D0CE30(__int64 a1, __int64 a2, __int64 a3)
{
  __int64 *v3; // rbx
  __int64 v6; // rsi
  __int64 result; // rax

  if ( *(_BYTE *)(a3 + 25) == 0 )
  {
    v3 = (__int64 *)a3;
    do
    {
      sub_140051570(a1, a2, v3[2]);
      v6 = *v3;
      result = sub_141750D04(v3);
      v3 = (__int64 *)v6;
    }
    while ( *(_BYTE *)(v6 + 25) == 0 );
  }
  return result;
}
